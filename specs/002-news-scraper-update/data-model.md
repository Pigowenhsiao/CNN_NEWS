# Data Model: Dual Source Financial News Scraper Update

## Entity: EnhancedNewsArticle

**Description**: Extends NewsArticle with additional validation fields and quality metrics for improved data integrity and performance tracking.

**Fields**:
- `id` (string): Unique identifier for the article (hashed URL or generated UUID)
- `title` (string): The headline of the news article (validated for length and content)
- `content` (string): Full text content of the article (validated for completeness and encoding)
- `url` (string): Original URL of the article (validated for proper URL format)
- `publication_date` (datetime): Publication date/time in UTC (format: YYYY-MM-DD HH:MM:SS, validated for presence and format)
- `source` (string): Source website (either "CNBC" or "CNN", validated for correct value)
- `scraped_at` (datetime): Timestamp when the article was scraped (automatically populated)
- `status` (string): Processing status (e.g., "pending", "processed", "filtered", "failed", validated for correct values)
- `quality_score` (float): Automated quality assessment score (0.0-1.0, calculated during processing)
- `similarity_hash` (string): Content hash for duplicate detection (generated during processing)
- `processing_time_ms` (int): Time taken to process this article in milliseconds (performance metric)
- `error_details` (object): Detailed error information if processing failed (structured error data)

**Validation Rules**:
- `title` must not be empty and must be under 500 characters
- `url` must be a valid URL format with http/https scheme
- `publication_date` must be within 72 hours of current time to be processed
- `source` must be either "CNBC" or "CNN"
- `content` must not be empty and must contain at least 100 characters
- `quality_score` must be between 0.0 and 1.0
- `similarity_hash` must be a valid SHA-256 hash string
- `processing_time_ms` must be a positive integer
- `error_details` must contain structured error information if status is "failed"

## Entity: ScrapingSession

**Description**: Represents a single scraping execution with performance metrics and error statistics for optimization tracking.

**Fields**:
- `session_id` (string): Unique identifier for the scraping session (generated UUID)
- `start_time` (datetime): When scraping started (automatically populated)
- `end_time` (datetime): When scraping completed (automatically populated)
- `duration_ms` (int): Total duration of scraping session in milliseconds (calculated)
- `total_articles_found` (int): Total number of articles identified during scraping (counted)
- `articles_processed` (int): Number of articles successfully processed (counted)
- `articles_failed` (int): Number of articles that failed processing (counted)
- `memory_peak_mb` (float): Peak memory usage during session in MB (monitored)
- `network_errors` (int): Count of network-related errors (counted)
- `parsing_errors` (int): Count of parsing-related errors (counted)
- `duplicate_articles` (int): Number of duplicate articles detected and skipped (counted)
- `sources_stats` (object): Statistics per source (e.g., count of articles, success rate, errors)
- `error_log` (list[ErrorLogEntry]): List of detailed error entries for troubleshooting

**Validation Rules**:
- `session_id` must be a valid UUID string
- `start_time` and `end_time` must be valid datetime objects
- `duration_ms` must be a positive integer
- `total_articles_found`, `articles_processed`, `articles_failed`, `network_errors`, `parsing_errors`, `duplicate_articles` must be non-negative integers
- `memory_peak_mb` must be a positive float
- `sources_stats` must contain valid statistics for each source
- `error_log` must contain valid ErrorLogEntry objects

## Entity: ErrorLogEntry

**Description**: Detailed error information with context, stack traces, and recovery attempts for improved troubleshooting.

**Fields**:
- `error_id` (string): Unique identifier for the error (generated UUID)
- `timestamp` (datetime): When the error occurred (automatically populated)
- `error_type` (string): Type of error (e.g., "NETWORK_ERROR", "PARSING_ERROR", "VALIDATION_ERROR")
- `severity` (string): Severity level (e.g., "DEBUG", "INFO", "WARN", "ERROR", "CRITICAL")
- `source_component` (string): Component where error originated (e.g., "CNN_PARSER", "CNBC_PARSER", "SCRAPER")
- `url` (string): URL being processed when error occurred (if applicable)
- `error_message` (string): Human-readable error message
- `stack_trace` (string): Full stack trace for debugging (if available)
- `context_data` (object): Additional context data for troubleshooting (request headers, response data, etc.)
- `recovery_attempted` (bool): Whether recovery was attempted (true/false)
- `recovery_successful` (bool): Whether recovery was successful (true/false)
- `recovery_action` (string): Action taken for recovery (if any)

**Validation Rules**:
- `error_id` must be a valid UUID string
- `timestamp` must be a valid datetime object
- `error_type` must be one of the predefined error types
- `severity` must be one of the predefined severity levels
- `source_component` must identify the component where error occurred
- `error_message` must not be empty
- `stack_trace` should contain stack trace information if available
- `context_data` should contain relevant context for troubleshooting
- `recovery_attempted` must be a boolean value
- `recovery_successful` must be a boolean value (only relevant if recovery was attempted)

## Entity: PerformanceMetrics

**Description**: Execution time, memory usage, and throughput statistics for optimization tracking.

**Fields**:
- `metrics_id` (string): Unique identifier for the metrics collection (generated UUID)
- `collection_time` (datetime): When metrics were collected (automatically populated)
- `execution_time_ms` (int): Total execution time in milliseconds (measured)
- `memory_usage_mb` (float): Current memory usage in MB (monitored)
- `peak_memory_mb` (float): Peak memory usage during session in MB (monitored)
- `articles_per_second` (float): Throughput rate of articles processed per second (calculated)
- `network_requests` (int): Total number of network requests made (counted)
- `successful_requests` (int): Number of successful network requests (counted)
- `failed_requests` (int): Number of failed network requests (counted)
- `average_request_time_ms` (float): Average time per network request in milliseconds (calculated)
- `connection_pool_utilization` (float): Percentage of connection pool in use (0.0-1.0, monitored)
- `cache_hit_rate` (float): Percentage of cache hits (0.0-1.0, calculated)
- `cpu_usage_percent` (float): CPU usage percentage (monitored if available)

**Validation Rules**:
- `metrics_id` must be a valid UUID string
- `collection_time` must be a valid datetime object
- `execution_time_ms` must be a positive integer
- `memory_usage_mb` and `peak_memory_mb` must be positive floats
- `articles_per_second` must be a positive float
- `network_requests`, `successful_requests`, `failed_requests` must be non-negative integers
- `average_request_time_ms` must be a positive float
- `connection_pool_utilization` must be between 0.0 and 1.0
- `cache_hit_rate` must be between 0.0 and 1.0
- `cpu_usage_percent` must be between 0.0 and 100.0 (if available)

## Entity: OutputFile

**Description**: The structured Markdown document containing all processed articles with required metadata and enhanced formatting.

**Fields**:
- `filename` (string): Generated filename following convention: US_News_yyyymmdd-hhmm.md (e.g., US_News_20251102-2023.md)
- `content` (string): Markdown formatted content with all articles (generated)
- `created_at` (datetime): Timestamp when file was created (automatically populated)
- `article_count` (int): Number of articles included in the file (counted)
- `total_words` (int): Total word count across all articles (calculated)
- `sources_coverage` (object): Coverage statistics by source (e.g., CNBC: 50%, CNN: 50%)
- `quality_metrics` (object): Overall quality metrics for the output (e.g., average quality score, duplicate rate)
- `generation_time_ms` (int): Time taken to generate output file in milliseconds (measured)

**Validation Rules**:
- `filename` must follow the specified date-time format and naming convention
- `content` must contain valid Markdown formatting with all required article fields
- `created_at` must be a valid datetime object
- `article_count` must match actual number of articles in content
- `total_words` must be a positive integer
- `sources_coverage` must contain valid coverage statistics for each source
- `quality_metrics` must contain valid quality metrics
- `generation_time_ms` must be a positive integer

## Relationships

- **EnhancedNewsArticle** ←→ **ScrapingSession**: Many-to-one (many articles belong to one session)
- **ErrorLogEntry** ←→ **ScrapingSession**: Many-to-one (many errors belong to one session)
- **PerformanceMetrics** ←→ **ScrapingSession**: Many-to-one (many metrics collections belong to one session)
- **EnhancedNewsArticle** ←→ **OutputFile**: Many-to-one (many articles belong to one output file)
- **ErrorLogEntry** ←→ **EnhancedNewsArticle**: One-to-many (one article can have multiple error entries)
- **PerformanceMetrics** ←→ **EnhancedNewsArticle**: One-to-many (one article can have multiple metrics entries)

## Entity Lifecycle

### EnhancedNewsArticle
1. **Created**: When article is first identified during scraping
2. **Processed**: When content is extracted and validated
3. **Filtered**: When article passes date filtering criteria
4. **Deduplicated**: When duplicate detection is performed
5. **Failed**: When processing encounters unrecoverable errors
6. **Completed**: When article is successfully added to output

### ScrapingSession
1. **Started**: When scraping process begins
2. **Processing**: While articles are being scraped and processed
3. **Completed**: When all articles have been processed
4. **Archived**: After session data is persisted for analysis

### ErrorLogEntry
1. **Logged**: When an error occurs during processing
2. **Reviewed**: When error is examined for troubleshooting
3. **Resolved**: When error cause is identified and addressed
4. **Archived**: After resolution for historical reference

### PerformanceMetrics
1. **Collected**: When metrics are gathered during processing
2. **Analyzed**: When metrics are examined for optimization
3. **Applied**: When metrics inform performance improvements
4. **Stored**: When metrics are persisted for trend analysis

### OutputFile
1. **Generated**: When output file is created
2. **Validated**: When file content is checked for completeness
3. **Stored**: When file is saved to filesystem
4. **Cleaned**: When file is automatically removed after 30 days

## Data Volume & Scale Assumptions

- **Daily Articles**: Expect 50-200 articles per source per day
- **Article Size**: Average 1-5KB per article (text content)
- **Session Duration**: Typically 1-5 minutes for complete scraping
- **Memory Usage**: Peak usage should remain under 500MB
- **Storage Growth**: Approximately 100KB-500KB per output file
- **Retention Period**: Files automatically cleaned after 30 days
- **Concurrent Sessions**: Support 1-3 concurrent scraping sessions
- **Error Rate**: Target <1% critical errors, <5% recoverable errors