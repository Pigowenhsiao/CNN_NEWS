#!/usr/bin/env python3
"""
Quick test to verify all modules can be imported correctly
"""

import sys
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_imports():
    print("Testing module imports...")
    
    try:
        # Test core modules
        from scraper import run_scraper
        print("✓ Successfully imported scraper module")
        
        # Test model modules
        from models.article import EnhancedNewsArticle
        from models.result import ScrapingResult
        print("✓ Successfully imported model modules")
        
        # Test parser modules
        from cnn_parser import get_cnn_articles, extract_cnn_content
        from cnbc_parser import get_cnbc_articles, extract_cnbc_content
        print("✓ Successfully imported parser modules")
        
        # Test utility modules
        from utils.date_filter import is_within_72_hours, parse_article_date
        from utils.logger import setup_logging, log_info, log_error
        from utils.rate_limiter import rate_limit, RateLimiter
        from utils.helpers import safe_request_with_retry, handle_request_failure
        print("✓ Successfully imported utility modules")
        
        # Test other modules
        from deduplication import remove_duplicates
        from output_writer import write_to_markdown, generate_filename
        print("✓ Successfully imported other core modules")
        
        print("\n🎉 All modules imported successfully!")
        print("The news scraper is ready to run using: ./news.sh")
        
    except Exception as e:
        print(f"✗ Error importing modules: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    test_imports()