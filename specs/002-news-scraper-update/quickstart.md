# Quickstart Guide: Dual Source Financial News Scraper Update

## Prerequisites

- Python 3.12.7 or higher
- pip package manager
- Virtual environment (recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install httpx beautifulsoup4 python-dateutil pytest
   ```

## Usage

### Basic Usage
To run the updated news scraper:

```bash
python src/scraper.py
```

This will:
1. Access both CNBC and CNN business sections
2. Extract articles published within the last 72 hours
3. Collect full content for qualifying articles
4. Generate a Markdown file with the naming convention `US_News_yyyymmdd-hhmm.md`

### Configuration
The scraper runs with default settings but can be configured through:
- Command-line arguments (for future enhancement)
- Environment variables (if needed for proxy, rate limiting, etc.)

## Output

The scraper generates a Markdown file in the current directory with the naming convention:
`US_News_yyyymmdd-hhmm.md`

Each article in the output includes:
- Source website (CNBC or CNN)
- Article title
- Publication date (formatted as YYYY-MM-DD HH:MM:SS)
- Original URL
- Full article content

## Running Tests

To run the unit tests:
```bash
pytest tests/unit/
```

To run the integration tests:
```bash
pytest tests/integration/
```

To run all tests:
```bash
pytest
```

## Troubleshooting

- If you encounter "429 Too Many Requests" errors, the application respects rate limits but you may want to add additional delays.
- If date filtering seems incorrect, check that your system time zone is set correctly.
- If content extraction fails for certain articles, it may be due to site structure changes; check the logs for specific errors.
- If memory usage exceeds 500MB, consider reducing concurrency or processing fewer articles at once.
- If duplicate articles appear in output, check that the deduplication algorithm is functioning correctly.

## Architecture Overview

The application follows a modular architecture:
- `scraper.py`: Main coordinator using asyncio for concurrent scraping
- `cnn_parser.py`: CNN-specific parsing logic
- `cnbc_parser.py`: CNBC-specific parsing logic  
- `date_filter.py`: Date/time parsing and 72-hour filtering logic
- `output_writer.py`: Markdown output formatting and file writing
- `deduplication.py`: Enhanced article deduplication logic with content similarity
- `error_handler.py`: Comprehensive error handling for all operations
- `performance_optimizer.py`: Performance optimization with connection pooling and caching
- `data_validator.py`: Data validation and default value assignment
- `utils/`: Utility functions and helpers including logger and rate limiter

## Performance Improvements

The updated scraper includes several performance enhancements:
- Connection pooling to reduce HTTP request overhead
- Caching of parsed content to avoid redundant processing
- Optimized concurrent scraping to reduce total execution time
- Memory usage monitoring to stay under 500MB limit
- Enhanced deduplication with content similarity analysis

## Error Handling Enhancements

The updated scraper includes improved error handling:
- Comprehensive exception handling for all network operations
- Detailed logging with appropriate severity levels (DEBUG, INFO, WARN, ERROR)
- Graceful recovery from network timeouts, DNS failures, and HTTP error responses
- Continue processing when individual articles fail, without affecting overall execution
- Centralized error handling module for consistent error processing

## Data Quality Improvements

The updated scraper includes enhanced data quality features:
- Enhanced deduplication algorithm considering content similarity in addition to title matching
- Comprehensive field validation with default values for missing information
- Consistent output formatting with proper escaping and encoding
- Handling of articles with very long content without memory issues
- Quality scoring for automated assessment of article completeness

## Testing Enhancements

The updated scraper includes additional testing capabilities:
- Unit tests for error handling functionality
- Unit tests for performance optimization features
- Unit tests for data validation and deduplication
- Integration tests for complete flow with error scenarios
- Performance benchmarks to verify optimization improvements