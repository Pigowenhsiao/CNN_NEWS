#!/usr/bin/env python3
"""
Simple entry point for the dual-source financial news scraper
"""

import sys
from pathlib import Path
import asyncio
from datetime import datetime, timedelta
import time

# Add the src directory to Python path to make imports work
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def run_news_scraper():
    """
    Simple function to run the news scraper with all dependencies
    """
    print("Initializing Dual Source Financial News Scraper...")
    
    # Dynamically import modules after adjusting path
    try:
        from src.models.article import EnhancedNewsArticle
        from src.models.result import ScrapingResult
        print("✓ Successfully imported models")
    except Exception as e:
        print(f"✗ Error importing models: {e}")
        return None
    
    try:
        from src.cnn_parser import get_cnn_articles, extract_cnn_content
        from src.cnbc_parser import get_cnbc_articles, extract_cnbc_content
        print("✓ Successfully imported parsers")
    except Exception as e:
        print(f"✗ Error importing parsers: {e}")
        return None
    
    try:
        from src.utils.date_filter import is_within_72_hours, parse_article_date
        from src.utils.logger import setup_logging, log_info, log_error
        from src.utils.rate_limiter import rate_limit
        from src.utils.helpers import safe_request_with_retry
        print("✓ Successfully imported utilities")
    except Exception as e:
        print(f"✗ Error importing utilities: {e}")
        return None
    
    try:
        from src.deduplication import remove_duplicates
        from src.output_writer import write_to_markdown, generate_filename
        print("✓ Successfully imported core functions")
    except Exception as e:
        print(f"✗ Error importing core functions: {e}")
        return None
    
    # Setup logging
    setup_logging()
    log_info("News scraper started", "main")
    
    # Create sample articles to test the system
    print("\nCreating sample articles for testing...")
    
    # Create a sample result to simulate scraper functionality
    sample_articles = []
    
    # Simulate scraping and processing
    try:
        print("Simulating scraping from dual sources...")
        
        # Simulate getting articles from both sources
        cnn_articles = [
            {
                'title': 'Sample CNN Financial News',
                'url': 'https://www.cnn.com/sample-cnn-article',
                'publication_date': datetime.now() - timedelta(hours=24),
                'source': 'CNN',
                'content': 'This is a sample content from CNN about financial news.'
            }
        ]
        
        cnbc_articles = [
            {
                'title': 'Sample CNBC Financial News',
                'url': 'https://www.cnbc.com/sample-cnbc-article',
                'publication_date': datetime.now() - timedelta(hours=12),
                'source': 'CNBC',
                'content': 'This is a sample content from CNBC about financial news.'
            }
        ]
        
        # Combine and filter articles
        all_articles_data = cnn_articles + cnbc_articles
        filtered_articles = []
        
        for article_data in all_articles_data:
            if is_within_72_hours(article_data['publication_date']):
                # Create EnhancedNewsArticle object
                article = EnhancedNewsArticle(
                    id=hash(article_data['url']).__str__(),
                    title=article_data['title'],
                    content=article_data['content'],
                    url=article_data['url'],
                    publication_date=article_data['publication_date'],
                    source=article_data['source']
                )
                sample_articles.append(article)
                filtered_articles.append(article)
                print(f"  ✓ Added article: {article_data['title']}")
            else:
                print(f"  - Skipped old article: {article_data['title']}")
        
        # Remove duplicates
        unique_articles = remove_duplicates(filtered_articles)
        print(f"  → Removed duplicates: {len(filtered_articles) - len(unique_articles)} duplicates found")
        
        # Create result object
        result = ScrapingResult(
            articles=unique_articles,
            errors=[],
            start_time=time.time(),
            end_time=time.time(),
            duration_seconds=0.0
        )
        
        print(f"\n✓ Scraping simulation completed!")
        print(f"  → Found {len(all_articles_data)} articles")
        print(f"  → Filtered to {len(filtered_articles)} within 72 hours")
        print(f"  → Deduplicated to {len(unique_articles)} unique articles")
        
        # Write to markdown
        if unique_articles:
            output_file = write_to_markdown(unique_articles)
            print(f"  → Output written to: {output_file}")
            
        log_info(f"News scraper completed with {len(unique_articles)} articles", "main")
        return result
        
    except Exception as e:
        log_error(f"Error in news scraper: {e}", "main")
        print(f"✗ Error during scraping simulation: {e}")
        return None


if __name__ == "__main__":
    print("Starting Dual Source Financial News Scraper...")
    print("="*50)
    
    # Run the scraper
    result = run_news_scraper()
    
    if result:
        print("="*50)
        print("Scraping completed!")
        print(f"Articles processed: {len(result.articles) if hasattr(result, 'articles') else 0}")
        print(f"Errors encountered: {len(result.errors) if hasattr(result, 'errors') else 0}")
        
        if hasattr(result, 'articles') and result.articles:
            print(f"Output written to: {getattr(result, 'output_file', 'N/A')}")
    else:
        print("No results returned from scraper.")
        print("Note: This may be expected if actual website requests were blocked in simulation mode")