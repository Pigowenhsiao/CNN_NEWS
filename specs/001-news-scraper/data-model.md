# Data Model: Dual Source Financial News Scraper

## Entity: NewsArticle

**Description**: Represents an individual news piece from either CNBC or CNN business sections

**Fields**:
- `id` (string): Unique identifier for the article
- `title` (string): The headline of the news article
- `content` (string): Full text content of the article
- `url` (string): Original URL of the article
- `publication_date` (datetime): Publication date/time in UTC (format: YYYY-MM-DD HH:MM:SS)
- `source` (string): Source website (either "CNBC" or "CNN")
- `scraped_at` (datetime): Timestamp when the article was scraped
- `status` (string): Processing status (e.g., "pending", "processed", "filtered", "failed")

**Validation Rules**:
- `title` must not be empty
- `url` must be a valid URL format
- `publication_date` must be within 72 hours of current time to be processed
- `source` must be either "CNBC" or "CNN"

## Entity: NewsSource

**Description**: Represents the origin of news articles with specific parsing logic

**Fields**:
- `name` (string): Name of the news source (e.g., "CNBC", "CNN")
- `base_url` (string): Base URL for the source
- `business_url` (string): Business section URL
- `parsing_rules` (object): CSS selectors and parsing logic specific to the source

**Validation Rules**:
- `name` must be unique
- `base_url` and `business_url` must be valid URL formats

## Entity: ScrapeResult

**Description**: Contains the collected data from the scraping process

**Fields**:
- `articles` (list[NewsArticle]): List of successfully scraped articles
- `errors` (list[object]): List of error objects with details
- `start_time` (datetime): When scraping started
- `end_time` (datetime): When scraping completed
- `source_stats` (object): Statistics per source (e.g., count of articles, success rate)

## Entity: OutputFile

**Description**: The structured Markdown document containing processed articles

**Fields**:
- `filename` (string): Generated filename following convention: US_News_yyyymmdd-hhmm.md
- `content` (string): Markdown formatted content with all articles
- `created_at` (datetime): Timestamp when file was created
- `article_count` (int): Number of articles included in the file

**Validation Rules**:
- `filename` must follow the specified date-time format
- `article_count` must match actual number of articles in content