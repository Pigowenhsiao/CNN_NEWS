# Dual Source Financial News Scraper

A robust Python application that scrapes financial news from both CNN Business and CNBC Business sections, filtering articles published within the last 72 hours and outputting them in a structured Markdown format.

## Features

- **Dual Source Scraping**: Simultaneously scrapes financial news from CNN Business and CNBC Business sections
- **Date Filtering**: Automatically filters articles to include only those published within the last 72 hours
- **Rate Limiting**: Implements 3-5 second delays between requests to avoid being blocked
- **Deduplication**: Removes duplicate articles based on title to prevent redundancy
- **Structured Output**: Generates Markdown files with consistent format and naming convention
- **Comprehensive Logging**: Implements all levels of logging for troubleshooting and monitoring

## Requirements

- Python 3.12.7 or higher
- Dependencies listed in `pyproject.toml` (httpx, beautifulsoup4, python-dateutil, pytest)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd dual-source-news-scraper
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

   Or manually using pip:
   ```bash
   pip install httpx beautifulsoup4 python-dateutil python-dotenv pytest
   ```

3. Create a .env file in the project root to configure your settings (optional, defaults will be used if not provided):
   ```bash
   touch .env
   ```
   Add configuration variables as needed (see Configuration section below).

## Usage

### Running the Scraper

Execute the scraper using the provided shell script:

```bash
./news.sh
```

This will activate the virtual environment and run the official scraper that actually fetches real news from the websites.

### Output

The scraper generates a Markdown file with the naming convention:
`US_News_yyyymmdd-hhmm.md`

Each article in the output includes:
- Source website (CNN or CNBC)
- Title
- Publication date (formatted as YYYY-MM-DD HH:MM:SS)
- Original URL
- News content

## Project Structure

```
src/
├── models/
│   ├── article.py          # EnhancedNewsArticle model
│   └── result.py           # ScrapingResult model
├── utils/
│   ├── date_filter.py      # Date processing and filtering
│   ├── logger.py           # Logging infrastructure
│   ├── rate_limiter.py     # Rate limiting implementation
│   └── helpers.py          # Helper functions
├── cnn_parser.py           # CNN-specific parsing logic
├── cnbc_parser.py          # CNBC-specific parsing logic
├── deduplication.py        # Article deduplication logic
├── output_writer.py        # Markdown output formatting
└── scraper.py              # Main scraper functionality
```

## Configuration

The scraper can be configured using environment variables loaded from a `.env` file. Create a `.env` file in the project root with the following optional variables:

```env
# CNN and CNBC Business URLs
CNN_BUSINESS_URL=https://www.cnn.com/business
CNBC_BUSINESS_URL=https://www.cnbc.com/business/

# Rate limiting configuration (in seconds)
RATE_LIMIT_MIN_DELAY=3.0
RATE_LIMIT_MAX_DELAY=5.0

# Date filtering (in hours)
DATE_FILTER_HOURS=72

# Request configuration
MAX_RETRIES=3

# Concurrency configuration
CONCURRENT_TASKS_LIMIT=3

# Output configuration
OUTPUT_FILE_PREFIX=US_News

# Max articles to process per source
MAX_ARTICLES_PER_SOURCE=10
```

If these variables are not set, the application will use the default values shown above.

The configuration includes:

- **Rate Limiting**: Configurable delays between requests to avoid being blocked
- **Date Filter**: Configurable time window in hours for filtering recent articles
- **Retry Mechanism**: Number of attempts to retry failed requests
- **Concurrency Control**: Maximum number of concurrent scraping tasks
- **Output Format**: Configurable prefix for the Markdown output files
- **Deduplication**: Based on article title normalization
- **Automatic Cleanup**: Removal of output files older than 30 days
- **Max Articles Per Source**: The maximum number of articles to process from each source (default: 10)

## Architecture

The system is designed with a modular architecture:

1. **Scraper Module**: Orchestrates the scraping process from both sources concurrently
2. **Parser Modules**: Source-specific logic for extracting articles and content
3. **Model Modules**: Data structures for articles and scraping results
4. **Utility Modules**: Helper functions for date parsing, rate limiting, logging, etc.
5. **Output Writer**: Formats and writes the final Markdown file

## Troubleshooting

If the scraper fails to extract news:

- Ensure the websites haven't changed their HTML structure
- Check if rate limiting is sufficient to avoid being blocked
- Verify network connectivity to the source websites
- Review logs for specific error messages

## License

This project is open source and available under the MIT License.