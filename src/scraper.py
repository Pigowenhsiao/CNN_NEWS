"""
Main scraper module for dual-source financial news scraping from CNBC and CNN
"""
import asyncio
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
import time
import sys
import os
from pathlib import Path
import asyncio

# Add src directory to path if needed
src_path = Path(__file__).parent
sys.path.insert(0, str(src_path))

# Import our modules
import sys
import os
from pathlib import Path

# Add the src directory to Python path for absolute imports
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

# Add the src directory to Python path for absolute imports
import sys
from pathlib import Path
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

# Import our modules
from models.article import EnhancedNewsArticle
from models.result import ScrapingResult
from cnn_parser import get_cnn_articles, extract_cnn_content
from cnbc_parser import get_cnbc_articles, extract_cnbc_content
from utils.date_filter import is_within_timeframe, parse_article_date
from utils.logger import log_info, log_error, setup_logging
from utils.rate_limiter import rate_limit
from utils.helpers import safe_request_with_retry
from deduplication import remove_duplicates
from output_writer import write_to_markdown
from config.loader import load_config


async def scrape_news_sources() -> ScrapingResult:
    """
    Main function to scrape news from both CNBC and CNN business sections
    """
    log_info("Starting news scraping process from dual sources", "scraper")
    start_time = time.time()
    
    all_articles: List[EnhancedNewsArticle] = []
    errors: List[Dict[str, Any]] = []
    
    # Scrape from both sources concurrently
    try:
        # Create tasks for both sources
        cnn_task = asyncio.create_task(_scrape_cnn())
        cnbc_task = asyncio.create_task(_scrape_cnbc())
        
        # Wait for both to complete
        cnn_result, cnbc_result = await asyncio.gather(cnn_task, cnbc_task, return_exceptions=True)
        
        # Process results from CNN scraping
        if isinstance(cnn_result, Exception):
            error_info = {
                "source": "CNN",
                "error": str(cnn_result),
                "timestamp": datetime.now().isoformat()
            }
            errors.append(error_info)
            log_error(f"CNN scraping failed: {str(cnn_result)}", "scraper")
        elif cnn_result:
            all_articles.extend(cnn_result)
            log_info(f"CNN scraping completed: {len(cnn_result)} articles", "scraper")
        
        # Process results from CNBC scraping
        if isinstance(cnbc_result, Exception):
            error_info = {
                "source": "CNBC",
                "error": str(cnbc_result),
                "timestamp": datetime.now().isoformat()
            }
            errors.append(error_info)
            log_error(f"CNBC scraping failed: {str(cnbc_result)}", "scraper")
        elif cnbc_result:
            all_articles.extend(cnbc_result)
            log_info(f"CNBC scraping completed: {len(cnbc_result)} articles", "scraper")
            
    except Exception as e:
        error_info = {
            "source": "scraper",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
        errors.append(error_info)
        log_error(f"Error in scraping coordination: {str(e)}", "scraper")
    
    # Remove duplicates
    unique_articles = remove_duplicates(all_articles)
    log_info(f"Deduplication complete: {len(unique_articles)} unique articles", "scraper")
    
    # Validate output requirements
    # (Implementation would go here for validating all articles meet output criteria)
    
    end_time = time.time()
    duration_seconds = end_time - start_time
    
    result = ScrapingResult(
        articles=unique_articles,
        errors=errors,
        start_time=start_time,
        end_time=end_time,
        duration_seconds=duration_seconds
    )
    
    log_info(f"Scraping completed in {duration_seconds:.2f}s", "scraper")
    
    return result


async def _scrape_cnn() -> List[EnhancedNewsArticle]:
    """
    Scrape articles from CNN business section
    """
    log_info("Starting CNN scraping", "cnn_scraper")
    
    articles = []
    
    try:
        config = load_config()
        
        # Limit concurrent requests using a semaphore
        semaphore = asyncio.Semaphore(config['concurrent_tasks_limit'])
        
        # Get article links from CNN business page
        cnn_article_links = await get_cnn_articles(url=config['cnn_business_url'])
        
        if not cnn_article_links:
            log_info("No articles found on CNN business page", "cnn_scraper")
            return articles
            
        log_info(f"Found {len(cnn_article_links)} potential articles on CNN", "cnn_scraper")
        
        # Process each article link with concurrency control
        for article_link in cnn_article_links:
            title = article_link.get('title', '')
            url = article_link.get('url', '')
            
            if not url:
                continue
                
            # Apply rate limiting before making request
            await rate_limit()
            
            # Extract content from the article page with concurrency control
            async with semaphore:  # Limit concurrent content extraction
                content_data = await extract_cnn_content(url)
            
            if content_data:
                # Check if article is within the configured timeframe
                pub_date_str = content_data.get('publication_date')
                pub_date = parse_article_date(pub_date_str, content_data['source']) if pub_date_str else None
                if pub_date and is_within_timeframe(pub_date):
                    # Create and add the article
                    article = EnhancedNewsArticle(
                        id=hash(url).__str__(),
                        title=content_data['title'],
                        content=content_data['content'],
                        url=content_data['url'],
                        publication_date=pub_date,
                        source=content_data['source']
                    )
                    articles.append(article)
                    log_info(f"Added CNN article: {title}", "cnn_scraper")
                else:
                    log_info(f"Skipped CNN article (too old): {title}", "cnn_scraper")
            else:
                log_info(f"Failed to extract content from CNN URL: {url}", "cnn_scraper")
                
    except Exception as e:
        log_error(f"CNN scraping error: {str(e)}", "cnn_scraper")
        raise  # Re-raise to be caught by the main function
    
    log_info(f"Completed CNN scraping: {len(articles)} articles", "cnn_scraper")
    return articles


async def _scrape_cnbc() -> List[EnhancedNewsArticle]:
    """
    Scrape articles from CNBC business section
    """
    log_info("Starting CNBC scraping", "cnbc_scraper")
    
    articles = []
    
    try:
        config = load_config()
        
        # Limit concurrent requests using a semaphore
        semaphore = asyncio.Semaphore(config['concurrent_tasks_limit'])
        
        # Get article links from CNBC business page
        cnbc_article_links = await get_cnbc_articles(url=config['cnbc_business_url'])
        
        if not cnbc_article_links:
            log_info("No articles found on CNBC business page", "cnbc_scraper")
            return articles
            
        log_info(f"Found {len(cnbc_article_links)} potential articles on CNBC", "cnbc_scraper")
        
        # Process each article link with concurrency control
        for article_link in cnbc_article_links:
            title = article_link.get('title', '')
            url = article_link.get('url', '')
            
            if not url:
                continue
                
            # Apply rate limiting before making request
            await rate_limit()
            
            # Extract content from the article page with concurrency control
            async with semaphore:  # Limit concurrent content extraction
                content_data = await extract_cnbc_content(url)
            
            if content_data:
                # Check if article is within the configured timeframe
                pub_date_str = content_data.get('publication_date')
                pub_date = parse_article_date(pub_date_str, content_data['source']) if pub_date_str else None
                if pub_date and is_within_timeframe(pub_date):
                    # Create and add the article
                    article = EnhancedNewsArticle(
                        id=hash(url).__str__(),
                        title=content_data['title'],
                        content=content_data['content'],
                        url=content_data['url'],
                        publication_date=pub_date,
                        source=content_data['source']
                    )
                    articles.append(article)
                    log_info(f"Added CNBC article: {title}", "cnbc_scraper")
                else:
                    log_info(f"Skipped CNBC article (too old): {title}", "cnbc_scraper")
            else:
                log_info(f"Failed to extract content from CNBC URL: {url}", "cnbc_scraper")
                
    except Exception as e:
        log_error(f"CNBC scraping error: {str(e)}", "cnbc_scraper")
        raise  # Re-raise to be caught by the main function
    
    log_info(f"Completed CNBC scraping: {len(articles)} articles", "cnbc_scraper")
    return articles


def run_scraper():
    """
    Synchronous function to run the scraper and handle command-line execution
    """
    # Setup logging
    setup_logging()
    
    # Run the scraping process
    result = asyncio.run(scrape_news_sources())
    
    # Write results to markdown
    if result.articles:
        output_file = write_to_markdown(result.articles)
        print(f"Successfully processed {len(result.articles)} articles")
        print(f"Output written to: {output_file}")
    else:
        print(f"No articles processed, but found {len(result.errors)} errors")
        
    # Print any errors
    if result.errors:
        print(f"Encountered {len(result.errors)} errors:")
        for error in result.errors:
            print(f"  - {error['source']}: {error['error']}")
    
    return result


async def run_scraper_async():
    """
    Asynchronous function to run the scraper (used by main entry point)
    """
    # Setup logging
    setup_logging()
    
    # Run the scraping process
    result = await scrape_news_sources()
    
    # Write results to markdown
    if result.articles:
        output_file = write_to_markdown(result.articles)
        print(f"Successfully processed {len(result.articles)} articles")
        print(f"Output written to: {output_file}")
    else:
        print(f"No articles processed, but found {len(result.errors)} errors")
        
    # Print any errors
    if result.errors:
        print(f"Encountered {len(result.errors)} errors:")
        for error in result.errors:
            print(f"  - {error['source']}: {error['error']}")
    
    return result