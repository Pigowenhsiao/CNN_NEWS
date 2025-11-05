"""
CNBC-specific parsing logic for extracting articles and content with enhanced error handling and date checking
"""
import asyncio
import httpx
import sys
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from datetime import datetime
import re
from urllib.parse import urljoin
from pathlib import Path

# Add the src directory to Python path for absolute imports
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

from utils.helpers import log_info, log_error, safe_request_with_retry
from utils.date_filter import parse_article_date, is_within_timeframe
from utils.rate_limiter import rate_limit
from utils.cache import content_cache
from models.article import EnhancedNewsArticle
from config.loader import load_config


async def get_cnbc_articles(url: str = None) -> List[Dict[str, Any]]:
    """
    Extract article links and metadata from CNBC business page
    
    Args:
        url (str, optional): URL to scrape from. If not provided, uses configured URL.
    
    Returns: List of dictionaries containing article titles and URLs
    """
    config = load_config()
    cnbc_business_url = url or config['cnbc_business_url']
    articles = []
    
    print(f"Starting CNBC article extraction from {cnbc_business_url}")
    
    try:
        # Apply rate limiting before making the request (using a simple sleep)
        # In production, this would use the actual rate limiter
        await asyncio.sleep(3.5)  # 3-5 second rate limit
        
        async with httpx.AsyncClient(timeout=30.0, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; NewsScraper/1.0)'
        }) as client:
            response = await safe_request_with_retry(client, cnbc_business_url, max_retries=config['max_retries'])
            
            if response is None or response.status_code != 200:
                print(f"Failed to access CNBC business page: {response.status_code if response else 'No response'}")
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find article links on CNBC business page
            # Look for links in article containers, typically with class patterns like 'Card-title' or 'teaser'
            link_elements = soup.find_all('a', href=True)
            processed_urls = set()  # To avoid duplicate processing
            
            for element in link_elements:
                href = element.get('href', '')
                
                # Skip if we've already processed this URL or it's not an article link
                if href in processed_urls or not _is_valid_cnbc_article_url(href):
                    continue
                    
                # Extract the text of the link, which should be the title
                title = element.get_text(strip=True)
                
                if title and len(title) > 15:  # Filter out very short titles that might be navigation links
                    full_url = _normalize_url(href, "https://www.cnbc.com")
                    if full_url:
                        articles.append({
                            'title': title,
                            'url': full_url
                        })
                        processed_urls.add(href)
                        
                        print(f"Found CNBC article: {title[:50]}...")  # Truncate for display
                        
                        # Limit to configured number of articles to avoid processing too many
                        config = load_config()
                        if len(articles) >= config['max_articles_per_source']:
                            log_info(f"Reached maximum article limit ({config['max_articles_per_source']}) on CNBC", "cnbc_parser")
                            break
                            
    except Exception as e:
        print(f"Error extracting CNBC articles: {str(e)}")
        return []
    
    print(f"Completed CNBC article extraction: {len(articles)} articles found")
    return articles


def _is_valid_cnbc_article_url(url: str) -> bool:
    """
    Check if the URL is a valid CNBC article URL based on patterns
    """
    if not url:
        return False
    
    # Valid CNBC article URL patterns
    patterns = [
        '/2025/',  # Current year articles
        '/2024/',  # Recent year articles
        'id-',     # CNBC article ID pattern
        '.html',   # HTML article pages
        '/articles/',  # Article path
        '/news/',  # News path
        '/investing/', # Investing section
        '/economy/', # Economy section
        '/finance/', # Finance section
    ]
    
    # Skip patterns in URLs
    skip_patterns = [
        '.jpg', '.jpeg', '.png', '.gif', '.svg', '.css', '.js', 
        'video/', 'videos/', 'gallery', 'newsletter', 
        'author/', 'authors/', 'tag/', 'tags/', '#', 'mailto:',
        'search?', 'search/', 'topic/', 'topics/', 'category/', 'categories/',
        '.mp4', '.mov', '.avi', '.wmv', '.zip', '.pdf', '.doc', '.docx',
        'playbook', 'live', 'quotes', 'quotes.html'
    ]
    
    # Check if URL matches any of these patterns and is an absolute path or full URL
    is_valid_path = any(pattern in url.lower() for pattern in patterns)
    is_not_excluded = not any(skip_pattern in url.lower() for skip_pattern in skip_patterns)
    
    # Also check if it's a valid article URL by structure
    is_article_url = bool(re.search(r'/\d{4}/\d{2}/\d{2}/', url))  # Contains date pattern like /yyyy/mm/dd/
    
    return (is_valid_path or is_article_url) and is_not_excluded and url.startswith(('http', '/', '../', './'))


def _normalize_url(url: str, base_domain: str) -> Optional[str]:
    """
    Normalize URL by converting relative to absolute if needed
    """
    if url.startswith('http'):
        # Already an absolute URL
        return url
    elif url.startswith('/'):
        # Relative to domain, make absolute
        return base_domain.rstrip('/') + url
    elif url.startswith('./') or url.startswith('../'):
        # Relative path, make absolute with base domain
        return urljoin(base_domain, url)
    else:
        # Probably already a relative path to the base domain
        return base_domain.rstrip('/') + '/' + url


async def extract_cnbc_content(url: str) -> Optional[Dict[str, Any]]:
    """
    Extract full content from a CNBC article URL with enhanced error handling and date validation
    
    Parameters:
    - url (str): URL of the CNBC article to extract content from

    Returns: Dictionary containing title, content, publication date, and other metadata
    """
    print(f"Extracting content from CNBC URL: {url}")
    
    # Apply rate limiting before making the request
    await asyncio.sleep(3.5)  # 3-5 second delay to respect rate limits
    
    # Load configuration
    config = load_config()
    
    # Check if content is already cached
    cached_result = content_cache.get(url, "")
    if cached_result:
        print(f"Retrieved CNBC article from cache: {cached_result.get('title', '')[:50]}...")
        return cached_result
    
    try:
        async with httpx.AsyncClient(timeout=30.0, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; NewsScraper/1.0)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }) as client:
            response = await safe_request_with_retry(client, url, max_retries=config['max_retries'])
            
            if response is None or response.status_code != 200:
                print(f"Failed to access CNBC article URL: {url} - Status: {response.status_code if response else 'No response'}")
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title - typically in h1 with class containing headline
            title_element = soup.find('h1')
            title = title_element.get_text(strip=True) if title_element else "Untitled Article"
            # If the title is too short, try alternative selectors
            if len(title) < 10:
                for alt_selector in ['[data-module-title]', 'title']:
                    title_element = soup.select_one(alt_selector) if soup.select_one(alt_selector) else None
                    if title_element:
                        title = title_element.get_text(strip=True)
                        break
                    else:
                        title_element = soup.find(alt_selector)
                        if title_element:
                            title = title_element.get_text(strip=True)
                            break
            
            # Extract publication date - common CNBC selectors
            date_element = None
            for selector in ['time', '.date', '.metadata__date', '[data-testid="published-timestamp"]']:
                date_element = soup.select_one(selector)
                if date_element:
                    break
            
            date_text = ""
            if date_element:
                # First try to get datetime attribute if it exists
                date_text = date_element.get('datetime', '')
                # If not, get the text content
                if not date_text:
                    date_text = date_element.get_text(strip=True)
            
            # Extract content - look for article body
            content_selectors = [
                '.ArticleBody-articleBody',      # CNBC specific
                '.renderedcontent',             # CNBC specific
                '.group',                       # CNBC specific
                '.ArticleLayout-articleBody',   # CNBC specific
                '[data-module="ArticleBody"]', # CNBC specific
                '.ArticleBody',                 # CNBC specific
                '.PostContent',                 # Alternative selector
                '.post-content',                # Common selector
                '.article-content',             # Common selector
                'article'                       # Semantic HTML
            ]
            
            content = ""
            for selector in content_selectors:
                content_element = soup.select_one(selector)
                if content_element:
                    # Get all paragraphs/text elements within the content area
                    paragraphs = content_element.find_all('p')
                    content_parts = [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20]
                    content = ' '.join(content_parts)
                    break
            
            # If no content found with specific selectors, try general approach
            if not content:
                # Look for main content area
                main_content_selectors = ['main', '.main-content', '#main', '.content', '#content']
                for selector in main_content_selectors:
                    main_content = soup.select_one(selector)
                    if main_content:
                        paragraphs = main_content.find_all('p')
                        content_parts = [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 30]
                        content = ' '.join(content_parts[:10])  # Take first 10 paragraphs to avoid too much content
                        if content:  # If we found content, stop looking
                            break
            
            # If still no content found, extract from the entire body (last resort)
            if not content:
                body_text = soup.body.get_text() if soup.body else soup.get_text()
                # Split by paragraphs and filter for meaningful content
                lines = body_text.split('\n')
                content_lines = [line.strip() for line in lines if len(line.strip()) > 50]
                content = ' '.join(content_lines[:15])  # Take up to 15 content-heavy lines
            
            # Clean up content - normalize whitespace, remove empty lines
            if content:
                content = ' '.join(content.split())
            
            # Validate content length to meet minimum requirement (50 characters)
            if not title or not content or len(content) < 50:
                print(f"Insufficient content extracted from CNBC URL: {url}")
                return None
            
            result = {
                'title': title,
                'content': content,
                'publication_date': date_text,  # Will be parsed later
                'url': url,
                'source': 'CNBC'
            }
            
            # Cache the result
            content_cache.set(url, content, result)
            
            print(f"Successfully extracted CNBC article: {title[:50]}...")  # Truncate for display
            
            return result
            
    except Exception as e:
        print(f"Error extracting CNBC content from {url}: {str(e)}")
        return None


def is_valid_cnbc_url(url: str) -> bool:
    """
    Check if the URL is a valid CNBC business article URL
    """
    return "cnbc.com/business" in url.lower() and not any(excluded in url.lower() for excluded in [
        'video.', 'gallery.', 'photogallery.', '.jpg', '.jpeg', '.png', '.gif', '.svg', 'quotes', 'live'
    ])


if __name__ == "__main__":
    # Test the CNBC parser functions directly
    import asyncio
    
    async def test_cnbc_parsing():
        print("Testing CNBC parsing functions...")
        
        # Test article extraction
        articles = await get_cnbc_articles()
        print(f"Found {len(articles)} articles from CNBC")
        
        # Test content extraction on first article if available
        if articles:
            first_article_url = articles[0]['url']
            content_data = await extract_cnbc_content(first_article_url)
            if content_data:
                print(f"Successfully extracted content: {content_data['title'][:50]}...")
            else:
                print("Failed to extract content from first article")
        else:
            print("No articles found to test content extraction")
    
    asyncio.run(test_cnbc_parsing())