"""
Article deduplication logic by title and content similarity to prevent duplicate entries in output
"""
import sys
import hashlib
from typing import List
from pathlib import Path

# Add the src directory to Python path for absolute imports
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

from models.article import EnhancedNewsArticle


def remove_duplicates(articles: List[EnhancedNewsArticle]) -> List[EnhancedNewsArticle]:
    """
    Remove duplicate articles based on title to prevent duplicate entries in output
    
    Args:
        articles (List[EnhancedNewsArticle]): List of articles to deduplicate
        
    Returns:
        List[EnhancedNewsArticle]: List of articles with duplicates removed
    """
    seen_titles = set()
    unique_articles = []
    
    for article in articles:
        # Normalize the title for comparison (case-insensitive, whitespace-normalized)
        normalized_title = ' '.join(article.title.lower().split())
        
        # If we haven't seen this normalized title, add the article to unique list
        if normalized_title not in seen_titles:
            seen_titles.add(normalized_title)
            unique_articles.append(article)
        else:
            # Log that a duplicate was found and skipped (only if logging is available)
            try:
                from .utils.logger import log_info
                log_info(f"Skipped duplicate article based on title: {article.title}", "deduplication")
            except ImportError:
                # If logging isn't available, just continue
                pass
    
    return unique_articles


def is_similar_content(content1: str, content2: str, threshold: float = 0.8) -> bool:
    """
    Check if two articles have similar content using a simple similarity algorithm
    
    Args:
        content1, content2 (str): Content to compare
        threshold (float): Similarity threshold (0.0-1.0); articles with similarity above threshold are considered duplicates
        
    Returns:
        bool: True if content is similar above threshold, False otherwise
    """
    if not content1 or not content2:
        return False
    
    # Simple similarity check using common words
    words1 = set(content1.lower().split())
    words2 = set(content2.lower().split())
    
    if not words1 or not words2:
        return False
    
    # Calculate Jaccard similarity coefficient
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    similarity = len(intersection) / len(union) if union else 0.0
    
    return similarity >= threshold


def generate_content_hash(content: str) -> str:
    """
    Generate a hash of content to identify potential duplicates
    
    Args:
        content (str): Content to hash
        
    Returns:
        str: SHA-256 hash string of the content
    """
    if not content:
        return ""
    
    # Normalize content by removing extra whitespace and converting to lowercase
    normalized_content = ' '.join(content.split()).lower()
    
    # Generate SHA-256 hash
    content_hash = hashlib.sha256(normalized_content.encode('utf-8')).hexdigest()
    
    return content_hash