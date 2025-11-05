# Quickstart Guide: Dual Source Financial News Scraper Update

## Overview
The Dual Source Financial News Scraper is a Python application that concurrently scrapes financial news from both CNN Business and CNBC Business sections. It filters articles published within the last 72 hours (configurable), deduplicates content, and outputs results to a structured Markdown file.

## Prerequisites
- Python 3.12.7 or higher
- pip package manager
- Git (for cloning the repository)

## Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd dual-source-news-scraper
```

### 2. Create and activate a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install httpx beautifulsoup4 python-dateutil python-dotenv pytest
```

### 4. Create a .env configuration file
Create a `.env` file in the project root with your desired configuration:
```env
# News source URLs
CNN_BUSINESS_URL=https://www.cnn.com/business
CNBC_BUSINESS_URL=https://www.cnbc.com/business/

# Rate limiting (in seconds)
RATE_LIMIT_MIN_DELAY=3.0
RATE_LIMIT_MAX_DELAY=5.0

# Date filtering (in hours)
DATE_FILTER_HOURS=72

# Request configuration
MAX_RETRIES=3

# Concurrency settings
CONCURRENT_TASKS_LIMIT=3
```

## Usage

### Running the Scraper
Execute the scraper using the shell script:
```bash
./news.sh
```

Or run directly using Python:
```bash
python -c "from src.scraper import run_scraper; run_scraper()"
```

### Output
The scraper generates a Markdown file with the naming convention:
`US_News_yyyymmdd-hhmm.md`

Each article in the output includes:
- Source website (CNN or CNBC)
- Title
- Publication date (formatted as YYYY-MM-DD HH:MM:SS)
- Original URL
- News content

## Configuration Options

### Changing News Sources
To scrape from different URLs, update the environment variables in your `.env` file:
```env
CNN_BUSINESS_URL=https://www.cnn.com/different-section
CNBC_BUSINESS_URL=https://www.cnbc.com/different-section
```

### Adjusting Date Filtering
To include articles from a different timeframe, change the `DATE_FILTER_HOURS`:
```env
DATE_FILTER_HOURS=48  # Include articles from last 48 hours only
```

### Modifying Rate Limits
To be more or less conservative with rate limiting:
```env
RATE_LIMIT_MIN_DELAY=5.0
RATE_LIMIT_MAX_DELAY=7.0
```

### Changing Retry Attempts
To modify the number of retry attempts (default is 3):
```env
MAX_RETRIES=5
```

### Controlling Concurrency
To limit how many requests are made simultaneously (default is 3):
```env
CONCURRENT_TASKS_LIMIT=5  # Maximum 5 concurrent scraping tasks
```

## Architecture Overview

The application follows a modular architecture with clear separation of concerns:

- **`src/config/loader.py`**: Handles loading and validation of configuration from environment variables
- **`src/cnn_parser.py` and `src/cnbc_parser.py`**: Source-specific scraping logic with multiple selector fallbacks
- **`src/utils/date_filter.py`**: Date validation and filtering logic
- **`src/utils/rate_limiter.py`**: Rate limiting with configurable delays
- **`src/deduplication.py`**: Article deduplication based on title and content similarity
- **`src/output_writer.py`**: Markdown output formatting
- **`src/scraper.py`**: Main coordination and execution logic with controlled concurrency

## Error Handling
- Network failures are handled with 3 retry attempts with exponential backoff
- Invalid content (less than 50 characters) is skipped with a warning
- Individual article failures don't stop the entire scraping process
- All errors and warnings are logged for debugging

## Troubleshooting

### Common Issues
1. **Rate Limiting**: If you receive 429 errors, increase the rate limit delays in your configuration
2. **Content Validation**: If articles are being skipped, verify they meet the 50 character minimum
3. **Parsing Failures**: If no articles are extracted, the target sites might have changed their HTML structure

### Verifying Installation
You can test that all modules import correctly:
```bash
python test_imports.py
```

### Logging
Check `scraper.log` for detailed execution logs and error information.