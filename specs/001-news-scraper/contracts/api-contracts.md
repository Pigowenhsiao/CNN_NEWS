# API Contracts: Dual Source Financial News Scraper

## Module: scraper.py

### Function: scrape_news_sources
**Description**: Main entry point to initiate scraping from both CNBC and CNN

**Signature**: 
```python
async def scrape_news_sources() -> ScrapeResult
```

**Parameters**: None

**Returns**: ScrapeResult object containing articles from both sources and any errors

**Contract**:
- Must initiate concurrent scraping of both CNBC and CNN business sections
- Must apply 72-hour date filter before processing articles
- Must return all successfully processed articles
- Must handle errors gracefully without stopping the entire process

## Module: cnn_parser.py

### Function: get_cnn_articles
**Description**: Extract article links and metadata from CNN business page

**Signature**:
```python
async def get_cnn_articles() -> List[Dict]
```

**Returns**: List of dictionaries containing article titles and URLs

### Function: extract_cnn_content
**Description**: Extract full content from a CNN article URL

**Signature**:
```python
async def extract_cnn_content(url: str) -> Dict
```

**Parameters**: 
- `url` (str): URL of the CNN article to extract content from

**Returns**: Dictionary containing title, content, publication date, and other metadata

## Module: cnbc_parser.py

### Function: get_cnbc_articles
**Description**: Extract article links and metadata from CNBC business page

**Signature**:
```python
async def get_cnbc_articles() -> List[Dict]
```

**Returns**: List of dictionaries containing article titles and URLs

### Function: extract_cnbc_content
**Description**: Extract full content from a CNBC article URL

**Signature**:
```python
async def extract_cnbc_content(url: str) -> Dict
```

**Parameters**:
- `url` (str): URL of the CNBC article to extract content from

**Returns**: Dictionary containing title, content, publication date, and other metadata

## Module: date_filter.py

### Function: is_within_72_hours
**Description**: Check if an article's publication date is within the last 72 hours

**Signature**:
```python
def is_within_72_hours(publication_date: datetime) -> bool
```

**Parameters**:
- `publication_date` (datetime): Publication date to check

**Returns**: True if date is within 72 hours of current time, False otherwise

### Function: parse_article_date
**Description**: Parse publication date from article content

**Signature**:
```python
def parse_article_date(date_string: str, source: str) -> datetime
```

**Parameters**:
- `date_string` (str): Raw date string from the article
- `source` (str): Source website identifier ("CNBC" or "CNN")

**Returns**: Parsed datetime object in UTC

## Module: output_writer.py

### Function: write_to_markdown
**Description**: Write processed articles to a formatted Markdown file

**Signature**:
```python
def write_to_markdown(articles: List[NewsArticle], filename: str = None) -> OutputFile
```

**Parameters**:
- `articles` (List[NewsArticle]): List of articles to write to file
- `filename` (str): Optional filename; if not provided, will use naming convention

**Returns**: OutputFile object with details about the created file

### Function: generate_filename
**Description**: Generate filename following the required naming convention

**Signature**:
```python
def generate_filename() -> str
```

**Returns**: Filename in format US_News_yyyymmdd-hhmm.md using current timestamp