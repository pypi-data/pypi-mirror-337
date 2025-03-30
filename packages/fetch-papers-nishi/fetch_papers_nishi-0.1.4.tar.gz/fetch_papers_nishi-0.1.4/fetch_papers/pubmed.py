"""
Module for interacting with the PubMed API using Biopython.
"""

import logging
import time
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from Bio import Entrez, Medline
from tqdm import tqdm

# Configure logger
logger = logging.getLogger(__name__)

# Type alias for paper data
PaperData = Dict[str, Union[str, List[str], Dict[str, str]]]


class PubMedFetcher:
    """Class to handle fetching and processing papers from PubMed."""

    def __init__(self, email: str = "nishichaudhary2001@gmail.com", tool: str = "FetchPapers") -> None:
        """
        Initialize the PubMed fetcher with required Entrez parameters.

        Args:
            email: Email to identify yourself to NCBI
            tool: Name of the tool/application
        """
        Entrez.email = email
        Entrez.tool = tool
        self.batch_size = 100  # Number of records to fetch in each batch

    def search_papers(self, query: str, max_results: int = 1000) -> List[str]:
        """
        Search for papers matching the query and return their PubMed IDs.

        Args:
            query: The search query in PubMed syntax
            max_results: Maximum number of results to return

        Returns:
            List of PubMed IDs for matching papers

        Raises:
            RuntimeError: If there's an error with the PubMed API
        """
        logger.debug(f"Searching PubMed with query: {query}")
        try:
            # Perform the search
            handle = Entrez.esearch(
                db="pubmed", term=query, retmax=max_results, usehistory="y"
            )
            record = Entrez.read(handle)
            handle.close()

            # Get the IDs of matching papers
            id_list = record["IdList"]
            logger.debug(f"Found {len(id_list)} papers matching query")

            # Also get the WebEnv and QueryKey for batch fetching if needed
            self.webenv = record.get("WebEnv", "")
            self.query_key = record.get("QueryKey", "")

            return id_list
        except Exception as e:
            logger.error(f"Error searching PubMed: {str(e)}")
            raise RuntimeError(f"Error searching PubMed: {str(e)}")

    def fetch_paper_details(self, id_list: List[str]) -> List[PaperData]:
        """
        Fetch detailed information about papers given their PubMed IDs.

        Args:
            id_list: List of PubMed IDs to fetch

        Returns:
            List of dictionaries containing paper details

        Raises:
            RuntimeError: If there's an error fetching paper details
        """
        logger.debug(f"Fetching details for {len(id_list)} papers")
        papers = []

        # Use WebEnv and QueryKey for batch fetching if available
        if hasattr(self, "webenv") and self.webenv and hasattr(self, "query_key") and self.query_key:
            papers = self._fetch_using_history()
        else:
            papers = self._fetch_by_ids(id_list)

        return papers

    def _fetch_using_history(self) -> List[PaperData]:
        """
        Fetch papers using WebEnv and QueryKey for efficient retrieval.

        Returns:
            List of paper data dictionaries
        """
        papers = []
        try:
            # Get the total count from the search
            handle = Entrez.esummary(
                db="pubmed", webenv=self.webenv, query_key=self.query_key, retmax=1
            )
            summary = Entrez.read(handle)
            handle.close()
            total = len(summary)
            
            logger.debug(f"Fetching {total} papers using history")
            
            # Fetch in batches
            for start in tqdm(range(0, total, self.batch_size), desc="Fetching papers"):
                try:
                    handle = Entrez.efetch(
                        db="pubmed",
                        webenv=self.webenv,
                        query_key=self.query_key,
                        retstart=start,
                        retmax=self.batch_size,
                        rettype="medline",
                        retmode="text",
                    )
                    records = Medline.parse(handle)
                    batch_papers = list(records)
                    papers.extend(self._process_papers(batch_papers))
                    handle.close()
                    
                    # Be gentle with the API
                    time.sleep(0.5)
                except Exception as e:
                    logger.warning(f"Error fetching batch starting at {start}: {str(e)}")
                    time.sleep(2)  # Wait longer on error
                    continue
                    
        except Exception as e:
            logger.error(f"Error using history to fetch papers: {str(e)}")
            raise RuntimeError(f"Error fetching papers: {str(e)}")
            
        return papers

    def _fetch_by_ids(self, id_list: List[str]) -> List[PaperData]:
        """
        Fetch papers by directly using their IDs.

        Args:
            id_list: List of PubMed IDs

        Returns:
            List of paper data dictionaries
        """
        papers = []
        for i in tqdm(range(0, len(id_list), self.batch_size), desc="Fetching papers"):
            batch_ids = id_list[i:i + self.batch_size]
            try:
                handle = Entrez.efetch(
                    db="pubmed", id=",".join(batch_ids), rettype="medline", retmode="text"
                )
                records = Medline.parse(handle)
                batch_papers = list(records)
                papers.extend(self._process_papers(batch_papers))
                handle.close()
                
                # Be gentle with the API
                time.sleep(0.5)
            except Exception as e:
                logger.warning(f"Error fetching batch {i//self.batch_size}: {str(e)}")
                time.sleep(2)  # Wait longer on error
                continue
                
        return papers

    def _process_papers(self, medline_records: List[Dict[str, Any]]) -> List[PaperData]:
        """
        Process Medline records into the required format.

        Args:
            medline_records: List of Medline records

        Returns:
            List of processed paper data
        """
        processed_papers = []
        
        for record in medline_records:
            # Basic paper information
            paper = {
                "pubmed_id": record.get("PMID", ""),
                "title": record.get("TI", "").strip(),
                "publication_date": self._extract_publication_date(record),
                "authors": record.get("AU", []),
                "affiliations": self._extract_affiliations(record),
                "corresponding_author_email": self._extract_email(record),
            }
            processed_papers.append(paper)
            
        return processed_papers

    def _extract_publication_date(self, record: Dict[str, Any]) -> str:
        """
        Extract and format the publication date from a Medline record.

        Args:
            record: Medline record

        Returns:
            Formatted publication date string
        """
        # Try different date fields in order of preference
        for date_field in ["PDAT", "DP", "DEP", "DA"]:
            if date_field in record:
                date_str = record[date_field]
                # Handle different date formats
                if "-" in date_str:  # YYYY-MM-DD format
                    return date_str
                elif "/" in date_str:  # YYYY/MM/DD format
                    return date_str
                else:  # Other formats
                    # Try to extract year and month if available
                    parts = date_str.split()
                    if len(parts) >= 2:
                        return f"{parts[0]} {parts[1]}"
                    elif len(parts) == 1:
                        return parts[0]
        
        return "Date unavailable"

    def _extract_affiliations(self, record: Dict[str, Any]) -> Dict[str, str]:
        """
        Extract author affiliations from a Medline record.

        Args:
            record: Medline record

        Returns:
            Dictionary mapping author names to their affiliations
        """
        affiliations = {}
        
        # Modern PubMed records may have structured affiliation data
        if "AD" in record:
            aff_data = record["AD"]
            if isinstance(aff_data, list):
                # Multiple affiliation strings
                authors = record.get("AU", [])
                # If we have both authors and affiliations
                if len(authors) > 0 and len(aff_data) > 0:
                    # Simple case: one affiliation per author
                    if len(authors) == len(aff_data):
                        for author, affiliation in zip(authors, aff_data):
                            affiliations[author] = affiliation
                    else:
                        # Otherwise, just use the first affiliation for all authors
                        # This is a simplification; in real data parsing would be more complex
                        for author in authors:
                            affiliations[author] = aff_data[0]
            elif isinstance(aff_data, str):
                # Single affiliation string, apply to all authors
                for author in record.get("AU", []):
                    affiliations[author] = aff_data
        
        # Fallback for older records
        if not affiliations and "AUID" in record and "AUFF" in record:
            author_ids = record["AUID"]
            author_affs = record["AUFF"]
            if len(author_ids) == len(author_affs):
                for author_id, affiliation in zip(author_ids, author_affs):
                    affiliations[author_id] = affiliation
        
        return affiliations

    def _extract_email(self, record: Dict[str, Any]) -> str:
        """
        Extract corresponding author email from a Medline record.

        Args:
            record: Medline record

        Returns:
            Email address or empty string if not found
        """
        # Look for email in the FAU (Full Author) or AD (Affiliation) fields
        email = ""
        
        # Check in affiliations field
        if "AD" in record:
            aff_data = record["AD"]
            if isinstance(aff_data, list):
                for aff in aff_data:
                    email = self._find_email_in_text(aff)
                    if email:
                        return email
            elif isinstance(aff_data, str):
                email = self._find_email_in_text(aff_data)
                if email:
                    return email
        
        # Check in abstract
        if "AB" in record:
            abstract = record["AB"]
            email = self._find_email_in_text(abstract)
            if email:
                return email
        
        # Check in investigator field
        if "INV" in record:
            investigators = record["INV"]
            if isinstance(investigators, list):
                for inv in investigators:
                    email = self._find_email_in_text(inv)
                    if email:
                        return email
            elif isinstance(investigators, str):
                email = self._find_email_in_text(investigators)
                if email:
                    return email
        
        return email

    def _find_email_in_text(self, text: str) -> str:
        """
        Find and extract an email address from text.

        Args:
            text: Text to search for email

        Returns:
            Email address or empty string if not found
        """
        import re
        
        # Common email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        
        if match:
            return match.group(0)
        return ""
