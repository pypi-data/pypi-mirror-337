"""Dataset creation module for PaperTuner."""
import os
import json
import time
import datetime
import re
import argparse
from enum import Enum
from typing import List, Optional
from pathlib import Path
from collections import defaultdict
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from datasets import Dataset, load_dataset
from huggingface_hub import create_repo, login, HfApi
import fitz  # PyMuPDF
import arxiv
# from openai import OpenAI # Removed openai import
from pydantic import BaseModel, Field
from google import genai # Added google genai import

from papertuner.config import (
    logger, RAW_DIR, PROCESSED_DIR,
    HF_TOKEN, HF_REPO_ID, GEMINI_API_KEY,
    setup_dirs
)
from papertuner.utils import api_call, save_json_file, validate_qa_pair


class ResearchPaperProcessor:
    """Processes research papers to create training datasets."""

    def __init__(
        self,
        raw_dir=RAW_DIR,
        processed_dir=PROCESSED_DIR,
        api_key=GEMINI_API_KEY, # Using GEMINI_API_KEY from config
        hf_token=HF_TOKEN,
        hf_repo_id=HF_REPO_ID
    ):
        """
        Initialize the paper processor.

        Args:
            raw_dir: Directory for raw PDF files
            processed_dir: Directory for processed data
            api_key: API key for LLM service
            api_base_url: Base URL for API calls
            hf_token: Hugging Face API token
            hf_repo_id: Hugging Face repository ID
        """
        self.raw_dir = Path(raw_dir)
        self.processed_dir = Path(processed_dir)
        self.api_key = api_key
        self.hf_token = hf_token
        self.hf_repo_id = hf_repo_id

        # Initialize Google GenAI client
        self.client = genai.Client(api_key=self.api_key) # Initialize GenerativeModel

        # Create directories
        setup_dirs()

        logger.info("ResearchPaperProcessor initialized with Google GenAI") # Updated log message

    def load_from_huggingface(self):
        """
        Load existing dataset from Hugging Face Hub.
        This will download the dataset and create local paper files.

        Returns:
            dict: Information about loaded dataset
        """
        try:
            logger.info(f"Loading dataset from Hugging Face: {self.hf_repo_id}")
            
            # Load the dataset
            hf_dataset = load_dataset(self.hf_repo_id, split="train")
            logger.info(f"Loaded dataset with {len(hf_dataset)} QA pairs")
            
            # Track unique papers and their QA pairs
            paper_data = defaultdict(list)
            processed_ids = set()
            
            # Group QA pairs by paper_id
            for item in hf_dataset:
                paper_id = item.get("paper_id", "")
                if not paper_id:
                    continue
                
                # Create QA pair
                qa_pair = {
                    "question": item.get("question", ""),
                    "answer": item.get("answer", ""),
                    "category": item.get("category", "General")
                }
                
                # Add to paper data
                paper_data[paper_id].append(qa_pair)
                processed_ids.add(paper_id)
            
            # Create paper files and manifest items
            manifest_items = []
            papers_created = 0
            
            for paper_id, qa_pairs in paper_data.items():
                # Skip if we don't have QA pairs for this paper
                if not qa_pairs:
                    continue
                
                # Get example QA pair for metadata
                example_qa = hf_dataset[
                    [i for i, item in enumerate(hf_dataset) if item.get("paper_id") == paper_id][0]
                ]
                
                # Create paper data
                paper_json = {
                    "metadata": {
                        "id": paper_id,
                        "title": example_qa.get("paper_title", ""),
                        "categories": example_qa.get("categories", [])
                    },
                    "qa_pairs": qa_pairs
                }
                
                # Save paper file
                filename = f"paper_{paper_id.split('/')[-1]}.json"
                file_path = self.processed_dir / "papers" / filename
                
                if save_json_file(paper_json, file_path, use_temp=True):
                    # Add to manifest
                    manifest_item = {
                        "id": paper_id,
                        "filename": filename,
                        "title": example_qa.get("paper_title", ""),
                        "processed_date": datetime.datetime.now().isoformat()
                    }
                    manifest_items.append(manifest_item)
                    papers_created += 1
            
            # Save manifest
            if manifest_items:
                manifest_path = self.processed_dir / "manifest.json"
                save_json_file(manifest_items, manifest_path)
                logger.info(f"Created manifest with {len(manifest_items)} papers")
            
            return {
                "success": True,
                "qa_pairs": len(hf_dataset),
                "papers": papers_created,
                "processed_ids": list(processed_ids)
            }
            
        except Exception as e:
            logger.error(f"Failed to load dataset from Hugging Face: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def has_been_processed(self, paper_id):
        """
        Check if a paper has already been processed.

        Args:
            paper_id: Unique identifier for the paper

        Returns:
            bool: True if already processed
        """
        processed_file = self.processed_dir / "papers" / f"paper_{paper_id.split('/')[-1]}.json"

        if processed_file.exists():
            try:
                with open(processed_file, 'r') as f:
                    data = json.load(f)
                    # Check for the new structure with multiple QA pairs
                    if (data.get("metadata") and
                        (data.get("qa_pairs") or data.get("qa"))):
                        logger.info(f"Paper {paper_id} already processed. Skipping.")
                        return True
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Found existing but invalid processed file for {paper_id}: {e}")
                return False

        return False

    def download_pdf(self, url, paper_id):
        """
        Download a PDF file.

        Args:
            url: URL of the PDF
            paper_id: Paper identifier

        Returns:
            Path: Path to downloaded file or None if failed
        """
        session = requests.Session()
        temp_path = self.raw_dir / f"temp_{paper_id.split('/')[-1]}.pdf"

        try:
            response = session.get(url, stream=True, timeout=10)
            response.raise_for_status()

            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)

            logger.info(f"Downloaded {url} to {temp_path}")
            return temp_path

        except requests.exceptions.RequestException as e:
            logger.warning(f"Download failed for {url}: {str(e)}")
            return None

    def extract_text(self, pdf_path):
        """
        Extract text from a PDF file.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            str: Extracted text
        """
        if not os.path.exists(pdf_path):
            return ""

        def _extract():
            try:
                doc = fitz.open(pdf_path)
                text = " ".join([page.get_text() for page in doc])
                logger.info(f"Text extracted from {pdf_path}")
                return text
            except Exception as e:
                logger.error(f"Extraction failed for {pdf_path}: {str(e)}")
                return ""

        try:
            with ThreadPoolExecutor() as executor:
                future = executor.submit(_extract)
                return future.result(timeout=30)
        except TimeoutError:
            logger.warning(f"Timeout extracting text from {pdf_path}")
            return ""
        except Exception as e:
            logger.error(f"Unexpected error extracting text: {str(e)}")
            return ""

    def generate_qa(self, paper_data, full_text, num_pairs=3): # Pass full_text instead of sections
        """
        Generate multiple QA pairs from a paper using structured output.

        Args:
            client: Google GenAI client instance
            paper_data: Metadata about the paper
            full_text: The text content of the paper
            num_pairs: Number of QA pairs to generate

        Returns:
            list: Generated QA pairs or None if generation fails
        """
        abstract = paper_data.get("abstract", "")
        # Removed: problem = sections.get("problem", "")
        # Removed: methodology = sections.get("methodology", "")
        # Removed: results = sections.get("results", "")

        # Extract key information about the paper
        paper_domain = paper_data.get("categories", [""])[0]
        paper_title = paper_data.get("title", "")

        # Prepare context
        context = f"""
        Title: {paper_title}
        Domain: {paper_domain}
        Abstract: {abstract}
        Full Text: {full_text[:5000]}...
        """
        prompt = f"""You are an expert research advisor helping assess a researcher's understanding of complex topics within a research field. Your goal is to generate questions that test general knowledge and critical thinking in the field, inspired by the discoveries and developments presented in a given research paper.  The person answering the question will likely be unfamiliar with the specific paper.

Based on the discoveries and developments described in this research paper, create {num_pairs} DISTINCT general research questions in the relevant field (e.g., biology, if the paper is in biology) and detailed answers. These questions should not be directly about the paper itself, but should use the paper's findings as a springboard to explore broader, complex topics in the field. Focus on questions that require reasoning and inference within the field, grounded in the research paper's content. **Crucially, do not generate questions or answers purely from general knowledge; all questions and answers must be rooted in and inspired by the content, discoveries, and context of the provided research paper.**

{context}

Your task is to:
1. Create {num_pairs} substantive question-answer pairs that assess general understanding and require reasoning about complex topics within the research domain, drawing inspiration from the paper's contributions.
2. Ensure each question encourages analytical thinking about the broader field and is not answerable by simply recalling facts from the provided paper or general knowledge alone, but requires applying the paper's insights to broader field concepts.
3. Prioritize questions that explore the 'how' and 'why' behind broader concepts in the field, informed by the research, focusing on underlying mechanisms, relationships, and implications within the domain.
4. Aim for questions that a researcher in the field would genuinely ponder to critically evaluate and understand complex aspects of the field, in light of the paper's advancements.
5. When possible, make sure each question belongs to a different category within the research field.

Each question should:
- Be technically specific to the research field and require reasoning to answer within that field (not general or vague, and not specifically about the paper itself).
- Focus on 'how' or 'why' questions related to broader concepts in the field, prompted by the paper's approach and findings.
- Explore underlying mechanisms, critical assumptions, or logical connections within the research domain, inspired by the paper's research.
- NOT be a simple question of fact or definition that can be looked up, or a question directly answerable from the paper, but instead require broader field knowledge informed by the paper.

Each answer should:
- Provide a detailed, reasoned explanation, going beyond surface-level information and paper-specific details to address the broader field question.
- Explain the 'why' and 'how' behind the concepts in the field, drawing upon the paper's insights as a starting point but extending to general field understanding.
- Discuss the reasoning process, potential assumptions, and implications of the answer within the larger context of the research domain.
- Address trade-offs, alternative interpretations, or limitations related to the field topic where relevant.
- Be thorough and provide a robust, reasoned response (at least 150-250 words), demonstrating a good understanding of the field's complexities inspired by the paper.

Avoid questions that are purely about factual recall or can be answered with general background knowledge without considering the nuances and advancements suggested by the research paper. Focus on questions that require reasoning about the field, based on, but extending beyond, the specific details and arguments presented in the paper.
"""

        class QuestionCategory(str, Enum):
            ARCHITECTURE = "Architecture & Design"
            IMPLEMENTATION = "Implementation Strategy & Techniques"
            METHODOLOGY = "Methodology & Approach"
            CHALLENGES = "Handling Specific Challenges"
            ADAPTATION = "Adaptation & Transfer"
            THEORY = "Theoretical Foundations"
            ANALYSIS = "Analysis & Interpretation"
            COMPARISON = "Comparative Assessment"
            ETHICS = "Ethical Considerations"
            FUTURE = "Future Directions"

        class QAPair(BaseModel):
            question: str = Field(..., description="The technical research question")
            answer: str = Field(..., description="Detailed answer to the question")
            category: QuestionCategory = Field(..., description="The category this question belongs to")

        class QAOutput(BaseModel):
            qa_pairs: List[QAPair] = Field(..., description="List of question-answer pairs generated from the paper")

        try:
            # Use structured output parsing
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',  # Tell the model to format the response as json
                    'response_schema': QAOutput,  # Try passing the pydantic class as response_schema
                },
            )

            #  response.text is the text, and we parse it using QAOutput
            qa_output = QAOutput.parse_raw(response.text)


            # Validate each QA pair
            validated_pairs = []
            for pair in qa_output.qa_pairs:
                pair_dict = {
                    "question": pair.question,
                    "answer": pair.answer,
                    "category": pair.category
                }
                if validate_qa_pair(pair_dict):
                    validated_pairs.append(pair_dict)

            return validated_pairs if validated_pairs else None

        except Exception as e:
            logger.error(f"QA generation failed: {e}")
            return None

    def process_paper(self, paper):
        """
        Process a single paper.

        Args:
            paper: Paper object from arxiv

        Returns:
            dict: Processed paper data or None if failed
        """
        # Check if paper has already been processed
        if self.has_been_processed(paper.entry_id):
            return None  # Skip this paper

        pdf_path = self.download_pdf(paper.pdf_url, paper.entry_id)
        if not pdf_path:
            logger.warning(f"Skipping paper {paper.entry_id} due to download failure.")
            return None

        text = self.extract_text(pdf_path)
        if not text:
            logger.warning(f"Skipping paper {paper.entry_id} due to text extraction failure.")
            return None

        paper_data = {
            "id": paper.entry_id,
            "title": paper.title,
            "authors": [str(a) for a in paper.authors],
            "abstract": paper.summary,
            "categories": paper.categories,
            "pdf_url": paper.pdf_url
        }

        # Generate multiple QA pairs
        qa_pairs = self.generate_qa(paper_data, text, num_pairs=3) # Pass 'text' not 'sections'
        if not qa_pairs:
            logger.warning(f"Skipping paper {paper.entry_id} due to failure to generate quality QA pairs.")
            return None

        # Return the processed paper data with multiple QA pairs
        result = {
            "metadata": {
                "id": paper_data["id"],
                "title": paper_data["title"],
                "categories": paper_data["categories"]
            },
            "qa_pairs": qa_pairs # No sections anymore
        }

        # Clean up the temp PDF
        try:
            if pdf_path and os.path.exists(pdf_path):
                os.remove(pdf_path)
        except OSError:
            pass

        return result

    def save_paper(self, data, paper_id):
        """
        Save processed paper data to disk.

        Args:
            data: Processed paper data
            paper_id: Paper identifier

        Returns:
            bool: Success status
        """
        filename = f"paper_{paper_id.split('/')[-1]}.json"
        file_path = self.processed_dir / "papers" / filename

        return save_json_file(data, file_path, use_temp=True)

    def load_processed_manifest(self):
        """
        Load the manifest of processed papers.

        Returns:
            list: List of paper IDs that have been processed
        """
        manifest_path = self.processed_dir / "manifest.json"
        if not manifest_path.exists():
            return []

        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
                return [item.get("id") for item in manifest if item.get("id")]
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to load manifest: {e}")
            return []

    def save_to_manifest(self, new_items):
        """
        Save new items to the manifest.

        Args:
            new_items: New items to add

        Returns:
            bool: Success status
        """
        manifest_path = self.processed_dir / "manifest.json"
        existing_items = []

        if manifest_path.exists():
            try:
                with open(manifest_path, 'r') as f:
                    existing_items = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to load existing manifest: {e}")
                # Start with an empty list if the file is corrupted

        # Combine existing and new items
        updated_manifest = existing_items + new_items

        # Write back to the manifest file
        return save_json_file(updated_manifest, manifest_path)

    def clear_processed_data(self):
        """
        Clears all processed paper data and the manifest.
        """
        papers_dir = self.processed_dir / "papers"
        manifest_path = self.processed_dir / "manifest.json"

        if papers_dir.exists():
            for filename in os.listdir(papers_dir):
                if filename.startswith("paper_") and filename.endswith(".json"):
                    file_path = papers_dir / filename
                    try:
                        os.remove(file_path)
                        logger.info(f"Deleted processed paper data: {filename}")
                    except OSError as e:
                        logger.error(f"Error deleting {filename}: {e}")

        if manifest_path.exists():
            try:
                os.remove(manifest_path)
                logger.info("Deleted processed papers manifest.")
            except OSError as e:
                logger.error(f"Error deleting manifest: {e}")
        else:
            logger.info("No manifest file found to delete.")

        logger.info("Processed data cleared.")


    def process_papers(self, max_papers=100, search_query=None, clear_processed_data=False): # Renamed force_reprocess to clear_processed_data
        """
        Process multiple papers from arXiv.

        Args:
            max_papers: Maximum number of papers to process
            search_query: ArXiv search query
            clear_processed_data: Clear existing data and start from scratch

        Returns:
            list: Processed paper manifest items
        """
        # Default search query for ML papers
        if search_query is None:
            search_query = " OR ".join([
                "machine learning",
                "deep learning",
                "large language models",
                "LLM",
                "natural language processing",
                "NLP",
                "transformers",
                "neural networks",
                "computer vision",
                "reinforcement learning",
                "generative models",
                "transfer learning",
                "few-shot learning",
                "zero-shot learning",
                "meta-learning"
            ])

        # Clear processed data if requested BEFORE loading manifest
        if clear_processed_data:
            logger.info("Clearing existing processed paper data before processing.")
            self.clear_processed_data()
            processed_ids = set() # Treat as if no papers processed yet
        else:
            # Load already processed papers to avoid duplication
            processed_ids = set(self.load_processed_manifest())
            logger.info(f"Found {len(processed_ids)} already processed papers")


        # Configure ArXiv client and search
        client = arxiv.Client()
        search = arxiv.Search(
            query=search_query,
            max_results=max_papers + len(processed_ids),  # Get more results to account for skipping
            sort_by=arxiv.SortCriterion.Relevance,
            sort_order=arxiv.SortOrder.Descending
        )

        new_manifest_items = []
        papers_processed = 0
        error_occurred = False

        # Process papers one by one
        for result in tqdm(client.results(search), desc="Processing papers"):
            # Skip if we've already processed this paper (only if not clearing data)
            if not clear_processed_data and result.entry_id in processed_ids: # Condition adjusted
                logger.info(f"Skipping already processed paper: {result.entry_id}")
                continue

            # Limit to the requested number of new papers
            if papers_processed >= max_papers:
                logger.info(f"Reached maximum number of papers to process: {max_papers}")
                break

            try:
                # Apply rate limiting
                if papers_processed > 0 and papers_processed % 5 == 0:
                    time.sleep(1 + 0.5 * (papers_processed % 3))

                # Process the paper
                paper = self.process_paper(result)
                if not paper:
                    logger.warning(f"Failed to process paper: {result.entry_id}. Skipping.")
                    continue

                # Save the processed paper
                saved = self.save_paper(paper, result.entry_id)
                if not saved:
                    logger.error(f"Failed to save paper: {result.entry_id}. Skipping manifest update.")
                    error_occurred = True
                    continue

                # Add to manifest
                new_manifest_item = {
                    "id": result.entry_id,
                    "filename": f"paper_{result.entry_id.split('/')[-1]}.json",
                    "title": result.title,
                    "processed_date": datetime.datetime.now().isoformat()
                }
                new_manifest_items.append(new_manifest_item)
                papers_processed += 1

                logger.info(f"Successfully processed paper {papers_processed}/{max_papers}: {result.entry_id}")

            except Exception as e:
                logger.error(f"Exception during paper processing for {result.entry_id}: {e}")
                error_occurred = True

        # Only update the manifest if we have new items
        if new_manifest_items and not clear_processed_data: # Do not save manifest if data was cleared and no new papers added in this run
            self.save_to_manifest(new_manifest_items)
            logger.info(f"Added {len(new_manifest_items)} papers to manifest")
        elif clear_processed_data:
            logger.info("Processed data cleared, manifest not updated (starting from scratch).")
        else:
            logger.info("No new papers were processed")

        if error_occurred:
            logger.error("Paper processing encountered errors.")

        return new_manifest_items

    def validate_dataset(self):
        """
        Validate the processed dataset.

        Returns:
            dict: Validation results
        """
        processed_files = list((self.processed_dir / "papers").glob("paper_*.json"))
        if not processed_files:
            raise FileNotFoundError(f"No processed files found in {self.processed_dir / 'papers'}")

        valid_count = 0
        issues = []

        for file in processed_files:
            try:
                with open(file, "r") as f:
                    data = json.load(f)

                    # Check for new format with multiple QA pairs
                    if "qa_pairs" in data and isinstance(data["qa_pairs"], list):
                        if not data["qa_pairs"]:
                            issues.append(f"Empty QA pairs in {file.name}")
                            continue

                        valid_count += 1
                        continue

                    # Check for old format with single QA pair
                    if not data.get("qa"):
                        issues.append(f"Missing QA pair in {file.name}")
                        continue

                    q = data["qa"].get("question", "").strip()
                    a = data["qa"].get("answer", "").strip()

                    if len(q) < 10 or len(a) < 50:
                        issues.append(f"Short QA pair in {file.name}")
                    else:
                        valid_count += 1

            except json.JSONDecodeError as e:
                issues.append(f"Invalid JSON format in {file.name}: {e}")
            except Exception as e:
                issues.append(f"Error validating {file.name}: {e}")

        return {
            "total_files": len(processed_files),
            "valid_entries": valid_count,
            "validation_issues": issues
        }

    def generate_statistics(self):
        """
        Generate statistics about the dataset.

        Returns:
            dict: Dataset statistics
        """
        processed_files = list((self.processed_dir / "papers").glob("paper_*.json"))

        stats = {
            "total_papers": len(processed_files),
            "total_qa_pairs": 0,
            "avg_question_length": 0,
            "avg_answer_length": 0,
            "category_distribution": defaultdict(int),
            "domain_breakdown": defaultdict(int)
        }

        total_q_chars = 0
        total_a_chars = 0
        qa_count = 0

        try:
            for file in processed_files:
                with open(file, "r") as f:
                    data = json.load(f)

                    # Extract domain and categories
                    categories = data["metadata"]["categories"]
                    if categories:
                        stats["category_distribution"][categories[0]] += 1
                        domain = categories[0].split(".")[0]
                        stats["domain_breakdown"][domain] += 1

                    # Process QA pairs
                    if "qa_pairs" in data and isinstance(data["qa_pairs"], list):
                        for qa in data["qa_pairs"]:
                            if qa.get("question") and qa.get("answer"):
                                total_q_chars += len(qa["question"])
                                total_a_chars += len(qa["answer"])
                                qa_count += 1

                                category = qa.get("category", "General")
                                stats["category_distribution"][f"QA: {category}"] += 1

                    # Process old format with single QA pair
                    elif "qa" in data and data["qa"].get("question") and data["qa"].get("answer"):
                        total_q_chars += len(data["qa"]["question"])
                        total_a_chars += len(data["qa"]["answer"])
                        qa_count += 1

        except Exception as e:
            logger.error(f"Error generating statistics: {e}")
            return None

        stats["total_qa_pairs"] = qa_count
        stats["avg_question_length"] = total_q_chars / qa_count if qa_count else 0
        stats["avg_answer_length"] = total_a_chars / qa_count if qa_count else 0

        return stats

    def push_to_hf(self, split_ratios=(0.8, 0.1, 0.1)):
        """
        Upload the dataset to Hugging Face Hub.

        Args:
            split_ratios: Train/val/test split ratios

        Returns:
            bool: Success status
        """
        if not self.hf_token:
            logger.warning("HF_TOKEN not set. Skipping upload.")
            return False

        if not self.hf_repo_id:
            logger.warning("HF_REPO_ID not set. Skipping upload.")
            return False

        processed_files = list((self.processed_dir / "papers").glob("paper_*.json"))
        qa_pairs = []
        metadata = defaultdict(list)

        try:
            for file in processed_files:
                with open(file, "r") as f:
                    data = json.load(f)

                    # Handle the case with multiple QA pairs
                    if "qa_pairs" in data and isinstance(data["qa_pairs"], list):
                        for qa in data["qa_pairs"]:
                            if qa.get("question") and qa.get("answer"):
                                qa_pairs.append({
                                    "question": qa["question"],
                                    "answer": qa["answer"],
                                    "category": qa.get("category", "General"),
                                    "paper_id": data["metadata"]["id"],
                                    "paper_title": data["metadata"]["title"],
                                    "categories": data["metadata"]["categories"]
                                })

                    # Handle the legacy case with a single QA pair
                    elif "qa" in data and data["qa"].get("question") and data["qa"].get("answer"):
                        qa_pairs.append({
                            "question": data["qa"]["question"],
                            "answer": data["qa"]["answer"],
                            "category": "General",
                            "paper_id": data["metadata"]["id"],
                            "paper_title": data["metadata"]["title"],
                            "categories": data["metadata"]["categories"]
                        })

                    # Aggregate metadata
                    metadata["titles"].append(data["metadata"]["title"])
                    metadata["paper_ids"].append(data["metadata"]["id"])
                    if "authors" in data["metadata"]:
                        metadata["authors"].extend(data["metadata"]["authors"])
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error while preparing dataset for HF upload: {e}")
            return False
        except Exception as e:
            logger.error(f"Error preparing dataset for HF upload: {e}")
            return False

        dataset = Dataset.from_list(qa_pairs)

        # Update the dataset card to include category information
        categories = set(item["category"] for item in qa_pairs if "category" in item)

        card_content = f"""\
    # Research Methodology QA Dataset

    ## Overview
    - Contains {len(qa_pairs)} validated question-answer pairs
    - Derived from {len(processed_files)} research papers
    - Domains: {', '.join(set(sum([item["categories"] for item in qa_pairs], [])))}

    ## Question Categories
    {', '.join(categories)}

    ## Fields
    - `question`: Technical research methodology question
    - `answer`: Detailed methodology answer
    - `category`: Question category/type
    - `paper_id`: Source paper identifier
    - `paper_title`: Title of the source paper
    - `categories`: arXiv categories
    """

        try:
            login(token=self.hf_token)
            create_repo(repo_id=self.hf_repo_id, repo_type="dataset", exist_ok=True)

            dataset.push_to_hub(
                self.hf_repo_id,
                commit_message=f"Add dataset with {len(dataset)} entries"
            )

            # Upload README separately
            with open("README.md", "w") as f:
                f.write(card_content)

            api = HfApi(token=self.hf_token)
            api.upload_file(
                path_or_fileobj="README.md",
                path_in_repo="README.md",
                repo_id=self.hf_repo_id,
                repo_type="dataset"
            )

            logger.info(f"Dataset uploaded to https://huggingface.co/datasets/{self.hf_repo_id}")
            return True  # Indicate upload success

        except Exception as e:
            logger.error(f"Failed to upload dataset to Hugging Face Hub: {e}")
            return False

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Create a dataset of QA pairs from research papers")

    parser.add_argument("--max-papers", type=int, default=100,
                        help="Maximum number of papers to process")
    parser.add_argument("--query", type=str, default=None,
                        help="ArXiv search query (default: ML-related topics)")
    parser.add_argument("--upload", action="store_true",
                        help="Upload the dataset to Hugging Face Hub")
    parser.add_argument("--hf-repo-id", type=str, default=None,
                        help="Hugging Face repository ID for upload")
    parser.add_argument("--validate", action="store_true",
                        help="Validate the dataset and print statistics")
    parser.add_argument("--clear-processed-data", action="store_true",
                        help="Clear all processed papers and manifest to start from scratch.")
    parser.add_argument("--load-from-hf", action="store_true",
                        help="Load existing dataset from HuggingFace before processing new papers")

    return parser.parse_args()


def main():
    """Main entry point for the dataset creation script."""
    args = parse_args()

    print("=" * 50)
    print(f"PaperTuner: Research Paper Dataset Creator")
    print("=" * 50)

    # Initialize processor with configuration
    processor = ResearchPaperProcessor(
        hf_repo_id=args.hf_repo_id or HF_REPO_ID
    )

    # Clear processed data if requested
    if args.clear_processed_data:
        print("Clearing all existing processed paper data...")
        processor.clear_processed_data()
        print("Processed data cleared.")
        print("=" * 50)
        print("Starting paper processing from scratch.")
        print("=" * 50)
    
    # Load existing dataset from HuggingFace if requested
    if args.load_from_hf and not args.clear_processed_data:
        print("Loading existing dataset from HuggingFace...")
        result = processor.load_from_huggingface()
        if result["success"]:
            print(f"Successfully loaded {result['qa_pairs']} QA pairs from {result['papers']} papers.")
            print("=" * 50)
        else:
            print(f"Failed to load dataset from HuggingFace: {result.get('error', 'Unknown error')}")
            print("Continuing with local dataset only.")
            print("=" * 50)

    # Process papers
    new_papers = processor.process_papers(
        max_papers=args.max_papers,
        search_query=args.query,
        clear_processed_data=args.clear_processed_data
    )

    if args.validate or args.upload:
        # Validate dataset
        validation = processor.validate_dataset()
        print(f"\nValidation Results:")
        print(f"- Total entries: {validation['total_files']}")
        print(f"- Valid QA pairs: {validation['valid_entries']}")
        print(f"- Issues found: {len(validation['validation_issues'])}")

        # Print dataset statistics
        stats = processor.generate_statistics()
        if stats:
            print("\nDataset Statistics:")
            print(f"- Total papers: {stats['total_papers']}")
            print(f"- Total QA pairs: {stats['total_qa_pairs']}")
            print(f"- Average question length: {stats['avg_question_length']:.1f} chars")
            print(f"- Average answer length: {stats['avg_answer_length']:.1f} chars")
            print("- Domain Breakdown:")
            for domain, count in sorted(stats["domain_breakdown"].items(), key=lambda x: x[1], reverse=True):
                print(f"  - {domain}: {count}")

    # Upload to Hugging Face if requested
    if args.upload:
        success = processor.push_to_hf()
        if success:
            print("\nDataset successfully uploaded to Hugging Face Hub!")
        else:
            print("\nFailed to upload dataset to Hugging Face Hub.")

    print("\n" + "=" * 50)
    if new_papers:
        print(f"Processing completed! Added {len(new_papers)} new papers to the dataset.")
    else:
        print("Processing completed! No new papers were added to the dataset.")
    print("=" * 50)


if __name__ == "__main__":
    main()
