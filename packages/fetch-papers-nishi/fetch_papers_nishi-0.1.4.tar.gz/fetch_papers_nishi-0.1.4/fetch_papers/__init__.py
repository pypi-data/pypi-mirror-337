"""
Fetch Papers - A tool to fetch research papers from PubMed and filter by author affiliation.

This package provides a modular approach to:
1. Fetching papers from PubMed API
2. Identifying authors affiliated with pharmaceutical/biotech companies
3. Generating structured output of the results
"""

__version__ = "0.1.0"

from fetch_papers.main import main
