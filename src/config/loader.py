"""
Configuration loader module for handling environment variables and defaults
"""
import os
from typing import Optional
from dotenv import load_dotenv


def load_config():
    """
    Load configuration from environment variables with .env file support
    Returns a dictionary containing configuration values for the scraper
    """
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    config = {
        # URLs for news sources
        'cnn_business_url': os.getenv('CNN_BUSINESS_URL', 'https://www.cnn.com/business'),
        'cnbc_business_url': os.getenv('CNBC_BUSINESS_URL', 'https://www.cnbc.com/business/'),
        
        # Rate limiting configuration (in seconds)
        'rate_limit_min_delay': float(os.getenv('RATE_LIMIT_MIN_DELAY', '3.0')),
        'rate_limit_max_delay': float(os.getenv('RATE_LIMIT_MAX_DELAY', '5.0')),
        
        # Date filtering configuration (in hours)
        'date_filter_hours': int(os.getenv('DATE_FILTER_HOURS', '72')),
        
        # Request configuration
        'max_retries': int(os.getenv('MAX_RETRIES', '3')),
        
        # Concurrency configuration
        'concurrent_tasks_limit': int(os.getenv('CONCURRENT_TASKS_LIMIT', '3')),
        
        # Output configuration
        'output_file_prefix': os.getenv('OUTPUT_FILE_PREFIX', 'US_News'),
    }
    
    # Validate URLs
    for key in ['cnn_business_url', 'cnbc_business_url']:
        if not _is_valid_url(config[key]):
            print(f"Warning: Invalid URL format for {key}: {config[key]}")
            # We don't raise an exception here to allow graceful fallback to defaults
            # but we could implement a more sophisticated validation approach
    
    return config


def _is_valid_url(url: str) -> bool:
    """
    Basic URL validation to check if the URL has a valid scheme and domain
    """
    if not url:
        return False
    return url.startswith(('http://', 'https://'))