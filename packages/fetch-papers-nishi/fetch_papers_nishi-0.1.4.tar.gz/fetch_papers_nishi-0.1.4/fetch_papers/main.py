"""
Main entry point for the fetch-papers tool.
"""

from fetch_papers.cli import cli

def main() -> None:
    """Execute the command-line interface."""
    cli()

if __name__ == "__main__":
    main()
