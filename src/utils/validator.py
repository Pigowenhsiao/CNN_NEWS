"""
Data validation and default value assignment module
"""
from typing import Any, Dict, Optional
from datetime import datetime
from .logger import log_warning, log_error


def validate_article_data(data: Dict[str, Any]) -> bool:
    """
    Validate required fields in scraped article data
    
    Args:
        data (Dict[str, Any]): Raw scraped article data to validate
        
    Returns:
        bool: True if all required fields are present and valid, False otherwise
    """
    required_fields = ['title', 'content', 'url', 'publication_date', 'source']
    
    for field in required_fields:
        if field not in data or data[field] is None or (isinstance(data[field], str) and data[field].strip() == ""):
            log_error(f"Missing or invalid required field '{field}' in article data", "data_validator")
            return False
    
    # Validate URL format (basic check)
    if not isinstance(data['url'], str) or not data['url'].startswith(('http://', 'https://')):
        log_error(f"Invalid URL format: {data['url']}", "data_validator")
        return False
        
    # Validate publication date
    if not isinstance(data['publication_date'], datetime):
        try:
            # Attempt to parse string date if needed
            if isinstance(data['publication_date'], str):
                from dateutil import parser as date_parser
                parsed_date = date_parser.parse(data['publication_date'])
                data['publication_date'] = parsed_date
            else:
                log_error(f"Publication date is not a valid datetime object: {type(data['publication_date'])}", "data_validator")
                return False
        except Exception as e:
            log_error(f"Could not parse publication date: {str(e)}", "data_validator")
            return False
    
    # Validate content length (ensure it's not too short to be meaningful)
    if len(data['content'].strip()) < 50:
        log_warning(f"Article content appears to be too short: only {len(data['content'])} characters", "data_validator")
    
    return True


def assign_default_values(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Assign default values for missing or invalid information in scraped data
    
    Args:
        data (Dict[str, Any]): Raw scraped data that may have missing values
        
    Returns:
        Dict[str, Any]: Data with default values assigned where needed
    """
    defaults = {
        'id': f"article_{hash(data.get('url', ''))}_{int(datetime.now().timestamp())}",
        'scraped_at': datetime.now(),
        'status': 'processed',
        'quality_score': 0.5,  # Default medium quality score
        'similarity_hash': None,
        'processing_time_ms': None
    }
    
    # Apply defaults for missing or invalid fields
    for field, default_value in defaults.items():
        if field not in data or data[field] is None:
            data[field] = default_value
            log_warning(f"Assigned default value for field '{field}'", "data_validator")
    
    # Handle missing title
    if 'title' not in data or not data['title'] or data['title'].strip() == '':
        data['title'] = 'Untitled Article'
        log_warning(f"Assigned default title: {data['title']}", "data_validator")
    
    # Handle missing content
    if 'content' not in data or not data['content'] or data['content'].strip() == '':
        data['content'] = 'No content could be extracted.'
        log_warning(f"Assigned default content", "data_validator")
    
    # Handle missing source
    if 'source' not in data or not data['source'] or data['source'].strip() == '':
        data['source'] = 'Unknown Source'
        log_warning(f"Assigned default source: {data['source']}", "data_validator")
    
    # Handle missing URL
    if 'url' not in data or not data['url'] or data['url'].strip() == '':
        data['url'] = '#'
        log_warning(f"Assigned default URL: {data['url']}", "data_validator")
    
    # Handle missing publication date
    if 'publication_date' not in data or not data['publication_date']:
        data['publication_date'] = datetime.now()
        log_warning(f"Assigned current date as publication date", "data_validator")
    
    return data


def sanitize_content(content: str) -> str:
    """
    Sanitize content for special characters that might affect Markdown formatting
    
    Args:
        content (str): Raw content to sanitize
        
    Returns:
        str: Sanitized content safe for Markdown formatting
    """
    if not isinstance(content, str):
        return ""
    
    # Remove or escape characters that might interfere with Markdown
    sanitized = content.replace('\r\n', '\n')  # Normalize line endings
    sanitized = sanitized.replace('\\', '\\\\')  # Escape backslashes
    sanitized = sanitized.replace('*', '\\*')  # Escape asterisks
    sanitized = sanitized.replace('_', '\\_')  # Escape underscores
    sanitized = sanitized.replace('#', '\\#')  # Escape hash symbols in case they're not intended as headers
    
    return sanitized


def validate_and_process_article(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Validate, assign defaults, and process article data in one function
    
    Args:
        data (Dict[str, Any]): Raw scraped article data
        
    Returns:
        Optional[Dict[str, Any]]: Processed article data if valid, None if invalid and cannot be salvaged
    """
    # Assign default values first to handle None/missing fields
    processed_data = assign_default_values(data)
    
    # Validate required fields
    if not validate_article_data(processed_data):
        log_error(f"Article failed validation after assigning defaults: {processed_data.get('title', 'Unknown')}", "data_validator")
        return None
    
    # Sanitize content for output
    processed_data['content'] = sanitize_content(processed_data['content'])
    
    # Generate similarity hash if not already present (simple approach using content)
    if processed_data.get('similarity_hash') is None:
        import hashlib
        content_bytes = processed_data['content'].encode('utf-8')
        hash_obj = hashlib.sha256(content_bytes)
        processed_data['similarity_hash'] = hash_obj.hexdigest()
    
    return processed_data


def validate_scraping_result(result: Dict[str, Any]) -> bool:
    """
    Validate the overall scraping result
    
    Args:
        result (Dict[str, Any]): Complete scraping result to validate
        
    Returns:
        bool: True if result structure is valid, False otherwise
    """
    required_top_level_keys = ['articles', 'errors', 'start_time', 'end_time']
    
    for key in required_top_level_keys:
        if key not in result:
            log_error(f"Missing required top-level key '{key}' in scraping result", "data_validator")
            return False
    
    articles = result['articles']
    if not isinstance(articles, list):
        log_error(f"Articles in scraping result is not a list: {type(articles)}", "data_validator")
        return False
    
    errors = result['errors']
    if not isinstance(errors, list):
        log_error(f"Errors in scraping result is not a list: {type(errors)}", "data_validator")
        return False
    
    # Validate that all articles have required fields
    for i, article in enumerate(articles):
        if not validate_article_data(article):
            log_warning(f"Article at index {i} failed validation: {article.get('title', 'Unknown')}", "data_validator")
    
    return True