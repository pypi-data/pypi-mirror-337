"""
Command-line interface for the fetch-papers tool.
"""

import csv
import logging
import sys
from typing import List, Optional, TextIO

import click
import pandas as pd

from fetch_papers.affiliation import AffiliationAnalyzer
from fetch_papers.pubmed import PaperData, PubMedFetcher

# Configure logger
logger = logging.getLogger(__name__)


@click.command()
@click.argument("query", required=True)
@click.option(
    "-d", "--debug", is_flag=True, help="Print debug information during execution"
)
@click.option(
    "-f", "--file", type=str, help="Specify the filename to save the results"
)
@click.option(
    "-m", "--max-results", type=int, default=1000, 
    help="Maximum number of results to retrieve (default: 1000)"
)
def cli(query: str, debug: bool, file: Optional[str], max_results: int) -> None:
    """
    Fetch research papers based on a user-specified query.

    Identifies papers with at least one author affiliated with a pharmaceutical
    or biotech company and returns the results in CSV format.

    QUERY: The search query in PubMed syntax.

    Example queries:
        - Simple term: diabetes
        - Multiple terms: diabetes AND insulin
        - Author search: Smith J[Author]
        - Date range: "2020/01/01"[Date - Publication] : "2020/12/31"[Date - Publication]
    """
    # Configure logging
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    if debug:
        logger.debug("Debug mode enabled")
        logger.debug(f"Query: {query}")

    try:
        # Fetch papers from PubMed
        fetcher = PubMedFetcher()
        paper_ids = fetcher.search_papers(query, max_results=max_results)

        if not paper_ids:
            logger.warning("No papers found matching the query")
            sys.exit(0)

        logger.info(f"Found {len(paper_ids)} papers matching the query")
        paper_data = fetcher.fetch_paper_details(paper_ids)

        # Filter and process papers
        analyzer = AffiliationAnalyzer()
        filtered_papers = []

        for paper in paper_data:
            authors = paper.get("authors", [])
            affiliations = paper.get("affiliations", {})
            email = paper.get("corresponding_author_email", "")

            # Identify non-academic authors and their companies
            non_academic_authors, company_names = analyzer.identify_company_authors(
                authors, affiliations, email
            )

            # Only keep papers with at least one non-academic author
            if non_academic_authors:
                filtered_paper = {
                    "PubmedID": paper.get("pubmed_id", ""),
                    "Title": paper.get("title", ""),
                    "Publication Date": paper.get("publication_date", ""),
                    "Non-academic Author(s)": "; ".join(non_academic_authors),
                    "Company Affiliation(s)": "; ".join(company_names),
                    "Corresponding Author Email": email
                }
                filtered_papers.append(filtered_paper)

        # Generate output
        if filtered_papers:
            df = pd.DataFrame(filtered_papers)
            logger.info(f"Filtered to {len(filtered_papers)} papers with non-academic authors")

            # Output to file or console
            # Only save to file if explicitly specified
            if file:
                try:
                    df['PubmedID'] = df['PubmedID'].astype(str)  # Ensure PubmedID is string
                    df.to_csv(file, index=False)
                    logger.info(f"Results saved to {file}")
                    # Always display results after saving
                    from tabulate import tabulate
                    print(f"\nSuccessfully saved {len(df)} results to {file}")
                    print("\nContents of results.csv:")
                    print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
                except Exception as e:
                    logger.error(f"Error saving results to {file}: {str(e)}")
                    print(f"Error saving results: {str(e)}")
            else:
                # Print to console in table format
                from tabulate import tabulate
                print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
        else:
            logger.warning("No papers found with non-academic authors")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        if debug:
            # In debug mode, print the full traceback
            import traceback
            logger.debug(traceback.format_exc())
        sys.exit(1)