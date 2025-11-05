# API Contracts: Dual Source Financial News Scraper Update

## Configuration Loading Interface

### Function: load_config
**Module**: `src/config/loader.py`
**Description**: Load configuration from environment variables with .env file support
**Signature**: `def load_config() -> dict`
**Returns**: Dictionary containing configuration values for the scraper
**Behavior**: 
- Attempts to load environment variables from .env file
- Provides default values if environment variables are not set
- Validates configuration values according to defined schema
**Requirements**:
- Must support loading from .env file if present
- Must provide default values for all configuration options
- Must validate URL formats
- Must validate numeric ranges (e.g., max_retries >= 1)
- Must log warnings for invalid configuration values

## Parser Module Interface Updates

### Module: `src/cnn_parser.py`
**Function**: `get_cnn_articles()`
**Signature**: `async def get_cnn_articles(url: str = None) -> List[Dict[str, Any]]`
**Behavior**: 
- Uses provided URL parameter or falls back to environment-configured URL
- Implements retry mechanism (3 attempts as per clarification)
- Uses multiple CSS selectors as fallbacks for parsing (as per clarification)
- Maintains all current functionality for extracting articles
- Handles rate limiting and error handling as before

### Module: `src/cnbc_parser.py`
**Function**: `get_cnbc_articles(url: str = None)`
**Signature**: `async def get_cnbc_articles(url: str = None) -> List[Dict[str, Any]]`
**Behavior**: 
- Uses provided URL parameter or falls back to environment-configured URL
- Implements retry mechanism (3 attempts as per clarification)
- Uses multiple CSS selectors as fallbacks for parsing (as per clarification)
- Maintains all current functionality for extracting articles
- Handles rate limiting and error handling as before

## Content Validation Interface

### Module: `src/cnn_parser.py` and `src/cnbc_parser.py`
**Function**: `extract_cnn_content()` and `extract_cnbc_content()`
**Signature**: `async def extract_cnn_content(url: str) -> Dict[str, Any]` and `async def extract_cnbc_content(url: str) -> Dict[str, Any]`
**Behavior**:
- Extracts content from the provided URL
- Validates content length (minimum 50 characters as per clarification)
- Returns None or appropriate error if content is below threshold
- Implements content validation with minimum length check (as per clarification)

## Rate Limiter Interface

### Module: `src/utils/rate_limiter.py`
**Class**: `RateLimiter`
**Signature**: `def __init__(self, min_delay: float = None, max_delay: float = None)`
**Behavior**:
- Respects configurable delay values from environment
- Supports min/max delay values as specified in configuration
- Implements rate limiting with 3-5 second delays by default

## Date Filtering Interface

### Module: `src/utils/date_filter.py`
**Function**: `is_within_timeframe()`
**Signature**: `def is_within_timeframe(pub_date: datetime, hours: int = None) -> bool`
**Behavior**:
- Uses configurable timeframe from environment variables
- Defaults to 72 hours if no configuration provided
- Maintains backward compatibility with existing 72-hour function

## Scraper Interface

### Module: `src/scraper.py`
**Function**: `scrape_news_sources()`
**Signature**: `async def scrape_news_sources() -> ScrapingResult`
**Behavior**:
- Limits concurrent tasks to 3 as per clarification
- Orchestrates scraping from both sources with controlled concurrency
- Implements error handling and retry logic as specified
- Returns ScrapingResult with statistics

## Configuration Schema

The application will support the following environment variables:

### CNN Configuration
- **CNN_BUSINESS_URL** (string): URL for CNN Business section (default: "https://www.cnn.com/business")

### CNBC Configuration
- **CNBC_BUSINESS_URL** (string): URL for CNBC Business section (default: "https://www.cnbc.com/business/")

### Rate Limiting Configuration
- **RATE_LIMIT_MIN_DELAY** (float): Minimum delay in seconds between requests (default: 3.0)
- **RATE_LIMIT_MAX_DELAY** (float): Maximum delay in seconds between requests (default: 5.0)

### Date Filtering Configuration
- **DATE_FILTER_HOURS** (integer): Maximum age of articles to process in hours (default: 72)

### Request Configuration
- **MAX_RETRIES** (integer): Maximum number of retries for failed requests (default: 3, per clarification)

### Concurrency Configuration
- **CONCURRENT_TASKS_LIMIT** (integer): Maximum concurrent scraping tasks (default: 3, per clarification)

## Error Handling Contracts

### Invalid Configuration
If configuration values are invalid:
1. The application shall log an error message
2. The application shall use default values for invalid configurations
3. The application shall continue operation with the valid configurations

### Missing Environment Variables
If environment variables are not set:
1. The application shall log an info message
2. The application shall use default values
3. The application shall continue normal operation

### Failed Content Extraction
If content extraction fails:
1. The application shall retry up to 3 times (per clarification)
2. The application shall use exponential backoff between retries
3. If all retries fail, the application shall log the error and continue with other articles

### Content Validation Failure
If content validation fails:
1. The application shall check for minimum 50 characters (per clarification)
2. If content is below threshold, the article shall be skipped
3. The application shall log a warning message