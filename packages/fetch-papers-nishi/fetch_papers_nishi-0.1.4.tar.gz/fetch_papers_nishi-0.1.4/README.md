# PubMed Pharma Paper Finder

A Python tool to fetch research papers from PubMed and filter for those with authors affiliated with pharmaceutical or biotech companies. Perfect for researchers and analysts tracking industry research contributions.

## Features

- 🔍 Search PubMed using standard query syntax
- 🤖 AI-powered query suggestions
- 🏢 Company affiliation detection
- 📊 Export results to CSV
- 🌐 Web interface and CLI support

## Quick Start

```bash
# Install from Test PyPI
pip install -i https://test.pypi.org/simple/ fetch-papers-nishi==0.1.0

# Run via CLI
get-papers-list "your search query" -f output.csv

# Or use in Python code
from fetch_papers import PubMedFetcher
fetcher = PubMedFetcher()
results = fetcher.search("cancer therapy")
```

## Web Interface

Access the web interface by running:
```bash
python main.py
```
Then open your browser to http://localhost:5000

## CLI Usage Examples

```bash
# Basic search
get-papers-list "cancer therapy"

# Specify max results
get-papers-list "diabetes" --max-results 50

# Save to CSV
get-papers-list "clinical trial" -f results.csv
```

## Advanced Search Tips

Use PubMed's powerful search syntax:
- Date range: `"2020/01/01"[Date - Publication] : "2020/12/31"[Date - Publication]`
- Author search: `Smith J[Author]`
- Publication type: `clinical trial[Publication Type]`
- Combined search: `diabetes AND (insulin OR metformin) NOT "type 1"`

## Development

1. Clone the repository
2. Install dependencies: `poetry install`
3. Run tests: `poetry run pytest`
4. Start web server: `python main.py`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Code style
- Pull request process
- Development setup

## Tools and Libraries Used

This project is built using the following tools and libraries:

- [**Python**](https://www.python.org/) (3.9+): Core programming language
- [**Poetry**](https://python-poetry.org/): Dependency management and packaging
- [**Biopython**](https://biopython.org/) (1.81+): Scientific tools for biological computation, used for PubMed API interaction via the Entrez module
- [**Flask**](https://flask.palletsprojects.com/) (3.1+): Web framework for the user interface
- [**Pandas**](https://pandas.pydata.org/) (2.0+): Data manipulation and analysis library, used for CSV processing
- [**Click**](https://click.palletsprojects.com/) (8.1+): Command-line interface creation toolkit
- [**scikit-learn**](https://scikit-learn.org/) (1.3+): Machine learning library used for AI-powered query suggestions
- [**Gunicorn**](https://gunicorn.org/) (23.0+): WSGI HTTP server for deploying the web application
- [**Bootstrap**](https://getbootstrap.com/) (5.3+): Frontend CSS framework for responsive design
- [**jQuery**](https://jquery.com/) (3.7+): JavaScript library for interactive features
- [**pytest**](https://pytest.org/) (7.0+): Testing framework
- [**tqdm**](https://tqdm.github.io/) (4.65+): Progress bar library
- [**PyInstaller**](https://pyinstaller.org/) (6.0+): Tool to bundle the application into a standalone executable


## PubMed API Usage

This tool uses the NCBI Entrez API through Biopython to fetch data from PubMed. It adheres to NCBI's [usage guidelines](https://www.ncbi.nlm.nih.gov/books/NBK25497/), including:

- No more than 3 requests per second
- Including an email address in API requests
- Properly citing NCBI as the data source

## Publishing to TestPyPI

The module is published on TestPyPI. You can find it here: [fetch-papers-nishi](https://test.pypi.org/project/fetch-papers-nishi/)

To install the package from TestPyPI:
```bash
pip install -i https://test.pypi.org/simple/ fetch-papers-nishi
```

To publish a new version:
1. Update version in pyproject.toml
2. Build the package: `poetry build`
3. Publish to TestPyPI: `poetry publish -r testpypi`

Current version: 0.1.2

## Contact & Links

Developed by Nishi Chaudhary
- Email: nishichaudhary2001@gmail.com
- LinkedIn: [Nishi Chaudhary](https://www.linkedin.com/in/nishi-chaudhary-3216a2201/)
- GitHub: [nchaudhary12](https://github.com/nchaudhary12)
- HackerRank: [nishichaudhary21](https://www.hackerrank.com/profile/nishichaudhary21)
- TestPyPI: [fetch-papers-nishi](https://test.pypi.org/project/fetch-papers-nishi/)

## Repository Protection

This repository is protected. While users can clone and use the code, they cannot modify or delete the repository contents. All changes must be approved by the repository owner.

## License

MIT License - see [LICENSE](LICENSE)