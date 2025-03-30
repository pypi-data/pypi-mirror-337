"""
Module for identifying and analyzing author affiliations.
"""

import logging
import re
from typing import Dict, List, Set, Tuple

# Configure logger
logger = logging.getLogger(__name__)

class AffiliationAnalyzer:
    """
    Class to analyze author affiliations and identify non-academic institutions.
    """
    
    def __init__(self) -> None:
        """Initialize the analyzer with pattern dictionaries."""
        # Common indicators of academic institutions
        self.academic_indicators: Set[str] = {
            "university", "college", "institute of technology", 
            "school of medicine", "medical school", "hospital",
            "clinic", "center for", "laboratory of", "national institute",
            "academy of", "polytechnic", "department of"
        }
        
        # Common indicators of commercial/pharma/biotech organizations
        self.company_indicators: Set[str] = {
            "inc", "incorporated", "corp", "corporation", "llc", "limited",
            "ltd", "pharma", "pharmaceuticals", "biotech", "therapeutics",
            "biosciences", "laboratories", "labs", "gmbh", "ag", "co.", "company",
            "bv", "sa", "nv", "holdings", "group", "plc", "research and development"
        }
        
        # Keywords that strongly indicate a company
        self.company_keywords: Set[str] = {
            "pfizer", "novartis", "roche", "merck", "johnson & johnson", 
            "sanofi", "glaxosmithkline", "gsk", "astrazeneca", "abbvie",
            "eli lilly", "gilead", "amgen", "biogen", "celgene", "bayer",
            "bristol-myers squibb", "boehringer", "novo nordisk", "takeda",
            "astellas", "daiichi", "eisai", "genentech", "regeneron", "vertex",
            "alexion", "alkermes", "biomarin", "incyte", "moderna", "biontech",
            "seagen", "seattle genetics"
        }
        
        # Common academic email domains
        self.academic_email_domains: Set[str] = {
            "edu", "ac.uk", "ac.jp", "edu.au", "ac.nz", "uni-", ".uni.", 
            "nih.gov", "ac.cn", "edu.cn", "ac.ir", "ac.kr"
        }
        
        # Email domains known to belong to companies
        self.company_email_domains: Set[str] = {
            "pfizer.com", "novartis.com", "roche.com", "merck.com", "jnj.com",
            "sanofi.com", "gsk.com", "astrazeneca.com", "abbvie.com", "lilly.com",
            "gilead.com", "amgen.com", "biogen.com", "celgene.com", "bayer.com",
            "bms.com", "boehringer-ingelheim.com", "novonordisk.com", "takeda.com"
        }

    def is_academic_affiliation(self, affiliation: str) -> bool:
        """
        Determine if an affiliation is academic.
        
        Args:
            affiliation: The affiliation string to check
            
        Returns:
            True if the affiliation appears to be academic, False otherwise
        """
        if not affiliation:
            return False
            
        affiliation_lower = affiliation.lower()
        
        # Check for academic indicators
        for indicator in self.academic_indicators:
            if indicator in affiliation_lower:
                return True
                
        return False

    def is_company_affiliation(self, affiliation: str) -> bool:
        """
        Determine if an affiliation is a company or commercial entity.
        
        Args:
            affiliation: The affiliation string to check
            
        Returns:
            True if the affiliation appears to be from a company, False otherwise
        """
        if not affiliation:
            return False
            
        affiliation_lower = affiliation.lower()
        
        # Check for company names
        for company in self.company_keywords:
            if company in affiliation_lower:
                return True
                
        # Check for company indicators
        for indicator in self.company_indicators:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(indicator) + r'\b'
            if re.search(pattern, affiliation_lower):
                # Make sure it's not clearly academic
                if not self.is_academic_affiliation(affiliation):
                    return True
                    
        return False

    def is_academic_email(self, email: str) -> bool:
        """
        Determine if an email address is from an academic institution.
        
        Args:
            email: The email address to check
            
        Returns:
            True if the email appears to be academic, False otherwise
        """
        if not email:
            return False
            
        email_lower = email.lower()
        
        # Check for academic email domains
        for domain in self.academic_email_domains:
            if domain in email_lower.split('@')[-1]:
                return True
                
        return False

    def is_company_email(self, email: str) -> bool:
        """
        Determine if an email address is from a company.
        
        Args:
            email: The email address to check
            
        Returns:
            True if the email appears to be from a company, False otherwise
        """
        if not email:
            return False
            
        email_lower = email.lower()
        
        # Check for company email domains
        for domain in self.company_email_domains:
            if domain in email_lower:
                return True
                
        # Check if the domain has a commercial TLD and isn't academic
        if not self.is_academic_email(email_lower):
            domain = email_lower.split('@')[-1]
            commercial_tlds = ['.com', '.co', '.io', '.ai']
            for tld in commercial_tlds:
                if domain.endswith(tld):
                    return True
                    
        return False

    def identify_company_authors(
        self, authors: List[str], affiliations: Dict[str, str], email: str
    ) -> Tuple[List[str], List[str]]:
        """
        Identify authors affiliated with companies and their company names.
        
        Args:
            authors: List of author names
            affiliations: Dictionary mapping author names to affiliation strings
            email: Corresponding author email
            
        Returns:
            Tuple containing (list of non-academic authors, list of company names)
        """
        non_academic_authors = []
        company_names = []
        
        # Check each author's affiliation
        for author in authors:
            affiliation = affiliations.get(author, "")
            
            if self.is_company_affiliation(affiliation):
                non_academic_authors.append(author)
                # Extract company name from affiliation
                company_name = self._extract_company_name(affiliation)
                if company_name and company_name not in company_names:
                    company_names.append(company_name)
        
        # If corresponding author has a company email but isn't already added
        if email and self.is_company_email(email):
            # Extract company name from email domain
            company_from_email = email.split('@')[-1].split('.')[0].title()
            if company_from_email and company_from_email not in company_names:
                company_names.append(company_from_email)
            
            # Add corresponding author if they can be identified and not already added
            # (This is a simplification - we'd need to know which author is the corresponding one)
        
        return non_academic_authors, company_names

    def _extract_company_name(self, affiliation: str) -> str:
        """
        Extract the company name from an affiliation string.
        
        Args:
            affiliation: The affiliation string
            
        Returns:
            The extracted company name or empty string if not found
        """
        if not affiliation:
            return ""
            
        # Try to match known company names first
        affiliation_lower = affiliation.lower()
        for company in self.company_keywords:
            if company in affiliation_lower:
                # Find the company name with proper capitalization
                start_idx = affiliation_lower.find(company)
                end_idx = start_idx + len(company)
                return affiliation[start_idx:end_idx]
        
        # Look for company identifiers
        for indicator in ["Inc.", "Corp.", "LLC", "Ltd.", "GmbH", "AG", "BV", "SA", "NV", "PLC"]:
            if indicator in affiliation:
                # Get the company name by taking words before the identifier
                parts = affiliation.split(indicator)[0].strip().split()
                # Take up to 3 words before the company identifier
                company_name = " ".join(parts[-3:]) if len(parts) >= 3 else " ".join(parts)
                return company_name
        
        # Fallback - return first "segment" of the affiliation
        segments = re.split(r'[,;]', affiliation)
        if segments:
            return segments[0].strip()
            
        return ""
