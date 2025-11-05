# Data Model: Dual Source Financial News Scraper Update

## Configuration Entity

### Config
- **cnn_business_url** (string): URL for CNN Business section (default: "https://www.cnn.com/business")
- **cnbc_business_url** (string): URL for CNBC Business section (default: "https://www.cnbc.com/business/")
- **max_retries** (integer): Maximum number of retries for failed requests (default: 3, per clarification)
- **rate_limit_min_delay** (float): Minimum delay in seconds between requests (default: 3.0)
- **rate_limit_max_delay** (float): Maximum delay in seconds between requests (default: 5.0)
- **date_filter_hours** (integer): Maximum age of articles to process in hours (default: 72)
- **concurrent_tasks_limit** (integer): Maximum number of concurrent scraping tasks (default: 3, per clarification)

### Validation Rules
1. **URL Validation**: Both cnn_business_url and cnbc_business_url must be valid HTTP/HTTPS URLs
2. **Rate Limit Range**: rate_limit_min_delay must be less than or equal to rate_limit_max_delay
3. **Positive Values**: All numeric values must be positive
4. **Content Validation**: Minimum content length of 50 characters (per clarification)
5. **Concurrent Tasks**: concurrent_tasks_limit must be between 1 and 10

### Relationships
- The configuration values are used by:
  - `src/cnn_parser.py` for initializing the scraping target
  - `src/cnbc_parser.py` for initializing the scraping target
  - `src/utils/rate_limiter.py` for rate limiting parameters
  - `src/utils/date_filter.py` for date filtering parameters
  - `src/scraper.py` for general configuration

### State Transitions
- Configuration is loaded once at application startup
- Configuration remains constant during execution
- Validation occurs at load time; invalid configurations cause startup to fail gracefully

## ScrapingResult Entity (Enhanced)

### Fields
- **articles** (List[EnhancedNewsArticle]): List of successfully processed articles
- **errors** (List[Dict[str, Any]]): List of error dictionaries with details
- **start_time** (float): Start time of scraping process (timestamp)
- **end_time** (float): End time of scraping process (timestamp)
- **duration_seconds** (float): Total duration of scraping in seconds
- **source_stats** (Dict[str, Any]): Statistics per source (e.g., count of articles, success rate)

## EnhancedNewsArticle Entity (Enhanced)

### Fields
- **id** (str): Unique identifier for the article
- **title** (str): Title of the news article
- **content** (str): Full content of the news article (minimum 50 characters per clarification)
- **url** (str): Original URL of the article
- **publication_date** (datetime): Date and time of publication
- **source** (str): Source website identifier ("CNN" or "CNBC")
- **scraped_at** (datetime): Time when article was scraped
- **status** (str): Processing status ("pending", "processed", "filtered", "failed")
- **quality_score** (float): Automated quality assessment (0.0-1.0)
- **similarity_hash** (str): Content hash for duplicate detection
- **processing_time_ms** (int): Processing time in milliseconds

### Validation Rules
1. **Content Length**: Content must be at least 50 characters (per clarification)
2. **Title Required**: Title must not be empty
3. **URL Format**: URL must be a valid HTTP/HTTPS URL
4. **Source Validation**: Source must be one of the recognized sources (CNN, CNBC)

### State Transitions
- "pending" → "processed" when scraping is successfully completed
- "pending" → "filtered" when article fails date check
- "pending" → "failed" when scraping encounters an error