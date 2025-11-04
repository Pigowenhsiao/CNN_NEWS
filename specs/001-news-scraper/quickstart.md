# Quickstart Guide: Dual Source Financial News Scraper

## Initial Setup

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd dual-source-financial-news-scraper
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Scraper

### Basic Execution
To run the scraper with default settings:
```bash
python -m src.scraper
```

### With Custom Output Filename
To specify a custom output filename:
```bash
python -m src.scraper --output "my_custom_news_file.md"
```

### With Verbose Logging
To enable debug-level logging:
```bash
python -m src.scraper --verbose
```

## Expected Output

The scraper generates a Markdown file with the naming convention:
`US_News_yyyymmdd-hhmm.md` (e.g., `US_News_20251103-1230.md`)

The output file will be located in the current directory and will contain:
- A header with the generation timestamp
- Each news article with its title, source, publication date, URL, and content
- A separator between articles

## Verification Steps

1. After running the scraper, verify the output file was created:
   ```bash
   ls -la US_News_*.md
   ```

2. Check the content of the output file:
   ```bash
   head -20 US_News_*.md
   ```

3. Verify that the file contains articles from both CNBC and CNN sources in the log output.

## Troubleshooting Common Issues

### Network Errors
- If you see "429 Rate limit exceeded" errors, the rate limiter is working correctly. The system waits 3-5 seconds between requests.
- If you see "404 Page not found" errors, check if the news sites have changed their URL structures.

### Date Filtering
- Articles older than 72 hours will be automatically filtered out. This is the expected behavior.
- To verify date filtering is working, look for log messages indicating articles were skipped due to age.

### Dependencies
- Ensure all required packages are installed by running `pip install -r requirements.txt`
- Make sure Python 3.12+ is installed (`python --version`)

## Example Output Structure

The generated Markdown file will have the following structure:

```markdown
# US Financial News Summary

Generated on: 2025-11-03 12:30:45

## Article Title 1
- **Source**: CNN
- **Published**: 2025-11-03 09:15:30
- **URL**: https://www.cnn.com/article-url-1

This is the content of article 1...

---

## Article Title 2
- **Source**: CNBC
- **Published**: 2025-11-03 10:30:45
- **URL**: https://www.cnbc.com/article-url-2

This is the content of article 2...

---
```

## Performance Expectations

- The scraper should complete within 5 minutes for a typical run
- At least 80% of identified articles should result in successful content extraction
- Memory usage should stay below 500MB during operation
- The system should successfully access both news sources at least 95% of the time under normal network conditions

## Cleaning Up

Output files are automatically cleaned up after 30 days, but you can manually remove old files if needed:
```bash
find . -name "US_News_*.md" -mtime +30 -delete
```

For questions or issues, please check the main documentation in the repository or submit an issue through the project's issue tracker.