"""
Module for providing AI-powered query suggestions for PubMed searches.

This module uses a combination of TF-IDF vectorization and pre-defined
medical domain knowledge to suggest relevant search queries based on user input.
"""

import re
import json
import logging
import os
from typing import List, Dict, Any
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Set up logging
logger = logging.getLogger(__name__)

# Common medical/pharmaceutical terms and concepts for fallback suggestions
PHARMA_CONCEPTS = [
    "clinical trials", "drug development", "pharmacokinetics", "pharmacodynamics",
    "adverse effects", "drug interactions", "bioavailability", "bioequivalence",
    "pharmaceutical formulation", "drug delivery", "therapeutic use",
    "drug resistance", "pharmacogenomics", "precision medicine",
    "randomized controlled trial", "phase I", "phase II", "phase III",
    "drug safety", "drug efficacy", "pharmacovigilance"
]

# Common pharma research terms by therapeutic area
THERAPEUTIC_AREAS = {
    "oncology": [
        "cancer therapy", "immunotherapy", "targeted therapy", "chemotherapy",
        "radiation therapy", "cancer biomarkers", "tumor microenvironment",
        "oncogenes", "cancer genomics", "metastasis", "angiogenesis"
    ],
    "neurology": [
        "alzheimer's disease", "parkinson's disease", "multiple sclerosis",
        "epilepsy", "stroke", "neuroprotection", "neurodegenerative diseases",
        "cognitive disorders", "brain-derived neurotrophic factor"
    ],
    "immunology": [
        "autoimmune disease", "inflammation", "immune response", "cytokines",
        "autoantibodies", "T cells", "B cells", "immunosuppression",
        "monoclonal antibodies", "immune checkpoint inhibitors"
    ],
    "cardiology": [
        "hypertension", "heart failure", "arrhythmia", "atherosclerosis",
        "myocardial infarction", "cardiovascular disease", "lipid metabolism",
        "thrombosis", "anticoagulants", "beta-blockers"
    ],
    "infectious disease": [
        "antibiotics", "antivirals", "vaccines", "antimicrobial resistance",
        "antifungals", "HIV", "hepatitis", "malaria", "tuberculosis", "coronavirus"
    ]
}

# Pharma company names to enhance suggestions
COMPANY_NAMES = [
    "pfizer", "novartis", "roche", "merck", "johnson & johnson", "sanofi", 
    "glaxosmithkline", "abbvie", "gilead", "amgen", "biogen", "genentech",
    "bayer", "astrazeneca", "eli lilly", "bristol myers squibb", "boehringer ingelheim",
    "moderna", "regeneron", "vertex"
]

# Path to save/load the TF-IDF vectorizer
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'data', 'tfidf_model.pkl')
CORPUS_PATH = os.path.join(os.path.dirname(__file__), 'data', 'query_corpus.json')

class QuerySuggester:
    """Class to generate and manage query suggestions for PubMed searches."""
    
    def __init__(self):
        """Initialize the QuerySuggester with TF-IDF vectorizer and corpus."""
        self.vectorizer = None
        self.corpus = []
        self.vectors = None
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        
        # Load or create TF-IDF vectorizer
        self._load_or_create_model()
    
    def _load_or_create_model(self):
        """Load existing TF-IDF model if available, otherwise create a new one."""
        try:
            if os.path.exists(MODEL_PATH) and os.path.exists(CORPUS_PATH):
                # Load existing model and corpus
                with open(MODEL_PATH, 'rb') as f:
                    self.vectorizer = pickle.load(f)
                
                with open(CORPUS_PATH, 'r') as f:
                    self.corpus = json.load(f)
                
                # Transform the corpus to get feature vectors
                self.vectors = self.vectorizer.transform(self.corpus)
                logger.info(f"Loaded existing model with {len(self.corpus)} queries")
            else:
                # Create a new model with initial corpus
                self._create_initial_corpus()
                self.vectorizer = TfidfVectorizer(
                    min_df=1, 
                    ngram_range=(1, 3),
                    stop_words='english'
                )
                self.vectors = self.vectorizer.fit_transform(self.corpus)
                
                # Save the model and corpus
                self._save_model()
                logger.info(f"Created new model with {len(self.corpus)} queries")
        except Exception as e:
            logger.error(f"Error loading/creating TF-IDF model: {e}")
            # Fallback to a simple model
            self._create_initial_corpus()
            self.vectorizer = TfidfVectorizer(min_df=1, ngram_range=(1, 2))
            self.vectors = self.vectorizer.fit_transform(self.corpus)
    
    def _create_initial_corpus(self):
        """Create an initial corpus of queries from domain knowledge."""
        self.corpus = []
        
        # Add general pharma concepts
        self.corpus.extend(PHARMA_CONCEPTS)
        
        # Add therapeutic area terms
        for area, terms in THERAPEUTIC_AREAS.items():
            self.corpus.extend(terms)
            # Add combinations with company names
            for company in COMPANY_NAMES:
                for term in terms[:3]:  # Limit combinations to avoid explosion
                    self.corpus.append(f"{term} {company}")
        
        # Add company-related queries
        for company in COMPANY_NAMES:
            self.corpus.append(f"{company} clinical trial")
            self.corpus.append(f"{company} drug development")
            self.corpus.append(f"{company} research")
    
    def _save_model(self):
        """Save the TF-IDF model and corpus to disk."""
        try:
            with open(MODEL_PATH, 'wb') as f:
                pickle.dump(self.vectorizer, f)
            
            with open(CORPUS_PATH, 'w') as f:
                json.dump(self.corpus, f)
            
            logger.info("Saved TF-IDF model and corpus")
        except Exception as e:
            logger.error(f"Error saving TF-IDF model: {e}")
    
    def _clean_query(self, query: str) -> str:
        """Clean and normalize the query text."""
        # Convert to lowercase
        query = query.lower()
        
        # Remove special PubMed syntax to get the core concepts
        query = re.sub(r'\[.*?\]', '', query)  # Remove field tags like [Author]
        query = re.sub(r'".*?"', lambda m: m.group(0).replace(' ', '_'), query)  # Preserve phrases
        query = re.sub(r'[():&|<>+\-]', ' ', query)  # Remove operators
        query = re.sub(r'\s+', ' ', query).strip()  # Normalize whitespace
        query = query.replace('_', ' ')  # Restore spaces in phrases
        
        return query
    
    def get_suggestions(self, query: str, num_suggestions: int = 5) -> List[str]:
        """
        Generate query suggestions based on user input.
        
        Args:
            query: The user's partial query string
            num_suggestions: Number of suggestions to return
            
        Returns:
            List of suggested query strings
        """
        if not query or len(query.strip()) < 2:
            # For very short queries, return popular/common queries
            suggestions = []
            # Add some general suggestions based on therapeutic areas
            for area, terms in list(THERAPEUTIC_AREAS.items())[:2]:
                suggestions.extend(terms[:2])
            return suggestions[:num_suggestions]
        
        try:
            # Clean the query
            cleaned_query = self._clean_query(query)
            
            # Transform the query using the vectorizer
            query_vector = self.vectorizer.transform([cleaned_query])
            
            # Calculate similarity to existing corpus
            similarities = cosine_similarity(query_vector, self.vectors).flatten()
            
            # Get indices of top similar queries
            top_indices = similarities.argsort()[:-num_suggestions-1:-1]
            
            # Return the corresponding queries
            suggestions = [self.corpus[i] for i in top_indices]
            
            # Add domain-specific suggestions if we have few results
            if len(suggestions) < num_suggestions:
                query_terms = cleaned_query.split()
                
                # Try to identify therapeutic areas in the query
                for area, terms in THERAPEUTIC_AREAS.items():
                    if any(area in cleaned_query for area in [area] + query_terms):
                        for term in terms:
                            if term not in suggestions and term != cleaned_query:
                                suggestions.append(term)
                                if len(suggestions) >= num_suggestions:
                                    break
                
                # Add some company-related suggestions if still needed
                if len(suggestions) < num_suggestions and len(query_terms) > 0:
                    for company in COMPANY_NAMES:
                        suggestion = f"{query_terms[0]} {company}"
                        if suggestion not in suggestions and suggestion != cleaned_query:
                            suggestions.append(suggestion)
                            if len(suggestions) >= num_suggestions:
                                break
            
            return suggestions[:num_suggestions]
            
        except Exception as e:
            logger.error(f"Error generating suggestions: {e}")
            # Fallback to basic suggestions
            return self._get_fallback_suggestions(query, num_suggestions)
    
    def _get_fallback_suggestions(self, query: str, num_suggestions: int) -> List[str]:
        """Provide basic fallback suggestions when the model fails."""
        suggestions = []
        query_lower = query.lower()
        
        # Check for therapeutic area matches
        for area, terms in THERAPEUTIC_AREAS.items():
            if area in query_lower or any(term in query_lower for term in terms[:3]):
                suggestions.extend([t for t in terms if t not in suggestions])
                break
        
        # Add some general terms if we still need more
        if len(suggestions) < num_suggestions:
            suggestions.extend([t for t in PHARMA_CONCEPTS if t not in suggestions])
        
        return suggestions[:num_suggestions]
    
    def add_query_to_corpus(self, query: str):
        """
        Add a successful query to the corpus for better future suggestions.
        
        Args:
            query: The query string to add
        """
        try:
            cleaned_query = self._clean_query(query)
            
            # Only add if it's not already in the corpus
            if cleaned_query and cleaned_query not in self.corpus:
                self.corpus.append(cleaned_query)
                
                # Update the vectorizer and vectors
                self.vectors = self.vectorizer.fit_transform(self.corpus)
                
                # Save the updated model
                self._save_model()
                logger.info(f"Added query to corpus: {cleaned_query}")
        except Exception as e:
            logger.error(f"Error adding query to corpus: {e}")


# Singleton instance for the application
_suggester = None

def get_suggester() -> QuerySuggester:
    """Get or create the QuerySuggester singleton instance."""
    global _suggester
    if _suggester is None:
        _suggester = QuerySuggester()
    return _suggester