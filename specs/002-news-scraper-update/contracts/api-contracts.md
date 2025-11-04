# API Contracts: Dual Source Financial News Scraper Update

## Module: scraper.py

### Function: scrape_news_sources
**Description**: Main entry point to initiate scraping from both CNBC and CNN with enhanced error handling and performance optimizations

**Signature**: 
```python
async def scrape_news_sources() -> ScrapingSession
```

**Parameters**: None

**Returns**: ScrapingSession object containing articles from both sources, error logs, and performance metrics

**Contract**:
- Must initiate concurrent scraping of both CNBC and CNN business sections
- Must apply 72-hour date filter before processing articles
- Must implement comprehensive error handling for all network operations
- Must log all significant events with appropriate severity levels
- Must continue processing when individual articles fail
- Must optimize concurrent scraping to reduce total execution time
- Must limit memory usage to under 500MB during normal operation
- Must return all successfully processed articles with error logs and performance metrics

## Module: cnn_parser.py

### Function: get_cnn_articles
**Description**: Extract article links and metadata from CNN business page with enhanced error handling

**Signature**:
```python
async def get_cnn_articles() -> List[Dict]
```

**Returns**: List of dictionaries containing article titles and URLs with error handling

### Function: extract_cnn_content
**Description**: Extract full content from a CNN article URL with enhanced error handling and performance optimizations

**Signature**:
```python
async def extract_cnn_content(url: str) -> Dict
```

**Parameters**: 
- `url` (str): URL of the CNN article to extract content from

**Returns**: Dictionary containing title, content, publication date, and other metadata with error handling

## Module: cnbc_parser.py

### Function: get_cnbc_articles
**Description**: Extract article links and metadata from CNBC business page with enhanced error handling

**Signature**:
```python
async def get_cnbc_articles() -> List[Dict]
```

**Returns**: List of dictionaries containing article titles and URLs with error handling

### Function: extract_cnbc_content
**Description**: Extract full content from a CNBC article URL with enhanced error handling and performance optimizations

**Signature**:
```python
async def extract_cnbc_content(url: str) -> Dict
```

**Parameters**:
- `url` (str): URL of the CNBC article to extract content from

**Returns**: Dictionary containing title, content, publication date, and other metadata with error handling

## Module: date_filter.py

### Function: is_within_72_hours
**Description**: Check if an article's publication date is within the last 72 hours with enhanced validation

**Signature**:
```python
def is_within_72_hours(publication_date: datetime) -> bool
```

**Parameters**:
- `publication_date` (datetime): Publication date to check

**Returns**: True if date is within 72 hours of current time, False otherwise with validation

### Function: parse_article_date
**Description**: Parse publication date from article content with enhanced error handling

**Signature**:
```python
def parse_article_date(date_string: str, source: str) -> datetime
```

**Parameters**:
- `date_string` (str): Raw date string from the article
- `source` (str): Source website identifier ("CNBC" or "CNN")

**Returns**: Parsed datetime object in UTC with error handling

## Module: output_writer.py

### Function: write_to_markdown
**Description**: Write processed articles to a formatted Markdown file with enhanced error handling and performance optimizations

**Signature**:
```python
def write_to_markdown(articles: List[EnhancedNewsArticle], filename: str = None) -> OutputFile
```

**Parameters**:
- `articles` (List[EnhancedNewsArticle]): List of articles to write to file
- `filename` (str): Optional filename; if not provided, will use naming convention

**Returns**: OutputFile object with details about the created file with error handling

### Function: generate_filename
**Description**: Generate filename following the required naming convention with enhanced validation

**Signature**:
```python
def generate_filename() -> str
```

**Returns**: Filename in format US_News_yyyymmdd-hhmm.md using current timestamp with validation

## Module: deduplication.py

### Function: remove_duplicates
**Description**: Remove duplicate articles based on content similarity in addition to title matching

**Signature**:
```python
def remove_duplicates(articles: List[EnhancedNewsArticle]) -> List[EnhancedNewsArticle]
```

**Parameters**:
- `articles` (List[EnhancedNewsArticle]): List of articles to deduplicate

**Returns**: List of articles with duplicates removed based on content similarity

## Module: error_handler.py

### Function: handle_request_failure
**Description**: Handle HTTP request failures with comprehensive error logging

**Signature**:
```python
def handle_request_failure(status_code: int, url: str) -> Dict[str, Any]
```

**Parameters**:
- `status_code` (int): HTTP status code from failed request
- `url` (str): URL of failed request

**Returns**: Dictionary containing error details with logging

### Function: log_error
**Description**: Log errors with comprehensive error handling and context

**Signature**:
```python
def log_error(error: Exception, context: str = "")
```

**Parameters**:
- `error` (Exception): Exception to log
- `context` (str): Context where error occurred

## Module: performance_optimizer.py

### Function: get_connection_pool
**Description**: Get connection pool for HTTP requests to reduce overhead

**Signature**:
```python
def get_connection_pool() -> httpx.AsyncClient
```

**Returns**: Configured httpx.AsyncClient with connection pooling

### Function: cache_parsed_content
**Description**: Cache parsed content to avoid redundant processing

**Signature**:
```python
def cache_parsed_content(key: str, content: Any) -> None
```

**Parameters**:
- `key` (str): Cache key
- `content` (Any): Content to cache

### Function: get_cached_content
**Description**: Get cached content if available

**Signature**:
```python
def get_cached_content(key: str) -> Any
```

**Parameters**:
- `key` (str): Cache key

**Returns**: Cached content or None if not available

## Module: data_validator.py

### Function: validate_article_data
**Description**: Validate all scraped data fields and provide default values for missing information

**Signature**:
```python
def validate_article_data(data: Dict) -> EnhancedNewsArticle
```

**Parameters**:
- `data` (Dict): Raw scraped data

**Returns**: Validated EnhancedNewsArticle with default values for missing information

### Function: format_article_markdown
**Description**: Format article content with proper escaping and encoding

**Signature**:
```python
def format_article_markdown(article: EnhancedNewsArticle) -> str
```

**Parameters**:
- `article` (EnhancedNewsArticle): Article to format

**Returns**: Properly formatted Markdown content with escaping and encoding