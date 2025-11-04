"""
CNN-specific parsing logic for extracting articles and content
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
from utils.date_filter import parse_article_date, is_within_72_hours
from utils.rate_limiter import rate_limit
from models.article import EnhancedNewsArticle


async def get_cnn_articles() -> List[Dict[str, Any]]:
    """
    Extract article links and metadata from CNN business page
    
    Returns: List of dictionaries containing article titles and URLs
    """
    cnn_business_url = "https://www.cnn.com/business"
    articles = []
    
    print(f"Starting CNN article extraction from {cnn_business_url}")
    
    try:
        # Apply rate limiting before making the request (using a simple sleep)
        # In production, this would use the actual rate limiter
        await asyncio.sleep(3.5)  # 3-5 second rate limit
        
        async with httpx.AsyncClient(timeout=30.0, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; NewsScraper/1.0)'
        }) as client:
            response = await client.get(cnn_business_url)
            
            if response.status_code != 200:
                print(f"Failed to access CNN business page: {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find article links on CNN business page
            # Looking for links with data-type="article" or those that contain article content in the URL
            link_elements = soup.find_all('a', href=True)
            processed_urls = set()  # To avoid duplicate processing
            
            for element in link_elements:
                href = element.get('href', '')
                
                # Skip if we've already processed this URL or it's not an article link
                if href in processed_urls or not _is_valid_cnn_article_url(href):
                    continue
                    
                # Extract the text of the link, which should be the title
                title = element.get_text(strip=True)
                
                if title and len(title) > 15:  # Filter out very short titles that might be navigation links
                    full_url = _normalize_url(href, "https://www.cnn.com")
                    if full_url:
                        articles.append({
                            'title': title,
                            'url': full_url
                        })
                        processed_urls.add(href)
                        
                        print(f"Found CNN article: {title[:50]}...")  # Truncate for display
                        
                        # Limit to 10 articles to avoid processing too many
                        if len(articles) >= 10:
                            break
                            
    except Exception as e:
        print(f"Error extracting CNN articles: {str(e)}")
        return []
    
    print(f"Completed CNN article extraction: {len(articles)} articles found")
    return articles


def _is_valid_cnn_article_url(url: str) -> bool:
    """
    Check if the URL is a valid CNN article URL based on patterns
    """
    if not url:
        return False
    
    # Valid CNN article URL patterns
    patterns = [
        '/2025/',  # Current year articles
        '/2024/',  # Recent year articles  
        '/article',
        '/news',
        '/business/',
    ]
    
    # Skip patterns in URLs
    skip_patterns = [
        '.jpg', '.jpeg', '.png', '.gif', '.svg', '.css', '.js', 
        'video/', 'videos/', 'gallery', 'newsletter', 
        'author/', 'authors/', 'tag/', 'tags/', '#', 'mailto:',
        'search?', 'search/', 'topic/', 'topics/', 'category/', 'categories/',
        '.mp4', '.mov', '.avi', '.wmv', '.zip', '.pdf', '.doc', '.docx'
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


async def extract_cnn_content(url: str) -> Optional[Dict[str, Any]]:
    """
    Extract full content from a CNN article URL
    
    Parameters:
    - url (str): URL of the CNN article to extract content from

    Returns: Dictionary containing title, content, publication date, and other metadata
    """
    print(f"Extracting content from CNN URL: {url}")
    
    # Apply rate limiting before making the request (using a simple sleep)
    await asyncio.sleep(3.5)  # 3-5 second rate limit
    
    try:
        async with httpx.AsyncClient(timeout=30.0, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; NewsScraper/1.0)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }) as client:
            response = await client.get(url)
            
            if response.status_code != 200:
                print(f"Failed to access CNN article URL: {url} - Status: {response.status_code}")
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title - typically in h1 tag
            title_element = soup.find('h1')
            title = title_element.get_text(strip=True) if title_element else "Untitled Article"
            
            # Extract publication date - common CNN selectors
            date_element = None
            for selector in ['time', '.update-time', '.article__date', '[data-js-hook="update-time"]']:
                if selector.startswith('.'):
                    date_element = soup.select_one(selector)
                elif selector.startswith('['):
                    date_element = soup.select_one(selector)
                else:
                    date_element = soup.find(selector)
                if date_element:
                    break
            
            date_text = ""
            if date_element:
                date_text = date_element.get('datetime', '') or date_element.get_text(strip=True)
            
            # Extract content - look for article body
            content_selectors = [
                'div[data-module="ArticleBody"]',  # CNN specific
                '.article__content',               # CNN specific
                '[data-editable="body"]',          # CNN specific
                '.zn-body__paragraph',             # CNN specific
                '.body-text',                      # Common class
                '.article-body',                   # Common class
                '.post-content',                   # Common class
                'article',                         # Semantic HTML
                '.entry-content',                  # WordPress standard
                '.storytext'                       # Alternative CNN selector
            ]
            
            content = ""
            for selector in content_selectors:
                content_elements = soup.select(selector)
                if content_elements:
                    # Get all paragraphs/text elements within the content area
                    content_parts = []
                    for elem in content_elements:
                        paragraphs = elem.find_all(['p', 'div'], recursive=False) or [elem]
                        for p in paragraphs:
                            text = p.get_text(strip=True)
                            if text and len(text) > 20:  # Only include meaningful text
                                content_parts.append(text)
                    if content_parts:
                        content = ' '.join(content_parts)
                        break
            
            # If no content found with specific selectors, try general approach
            if not content:
                for selector in ['main', '.main-content', '#main', '.content', '#content']:
                    main_content = soup.select_one(selector)
                    if main_content:
                        paragraphs = main_content.find_all('p')
                        content_parts = [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 30]
                        content = ' '.join(content_parts[:10])  # Take first 10 paragraphs to avoid too much content
                        if content:  # If we found content, stop looking
                            break
            
            # Clean up content - normalize whitespace, remove empty lines
            if content:
                content = ' '.join(content.split())
            
            if not title or not content:
                print(f"Insufficient content extracted from CNN URL: {url}")
                return None
            
            print(f"Successfully extracted CNN article: {title[:50]}...")  # Truncate for display
            
            return {
                'title': title,
                'content': content,
                'publication_date': date_text,  # Will be parsed later
                'url': url,
                'source': 'CNN'
            }
            
    except Exception as e:
        print(f"Error extracting CNN content from {url}: {str(e)}")
        return None


def is_valid_cnn_url(url: str) -> bool:
    """
    Check if the URL is a valid CNN business article URL
    """
    return "cnn.com/business" in url.lower() and not any(excluded in url.lower() for excluded in [
        'video.', 'gallery.', 'photogallery.', '.jpg', '.jpeg', '.png', '.gif', '.svg'
    ])


if __name__ == "__main__":
    # Test the CNN parser functions directly
    import asyncio
    
    async def test_cnn_parsing():
        print("Testing CNN parsing functions...")
        
        # Test article extraction
        articles = await get_cnn_articles()
        print(f"Found {len(articles)} articles from CNN")
        
        # Test content extraction on first article if available
        if articles:
            first_article_url = articles[0]['url']
            content_data = await extract_cnn_content(first_article_url)
            if content_data:
                print(f"Successfully extracted content: {content_data['title'][:50]}...")
            else:
                print("Failed to extract content from first article")
        else:
            print("No articles found to test content extraction")
    
    asyncio.run(test_cnn_parsing())