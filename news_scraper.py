#!/usr/bin/env python3
"""
Simple entry point for the dual-source financial news scraper
"""

import asyncio
import sys
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))
sys.path.insert(0, str(src_path.parent))  # Add parent directory too

def run_news_scraper():
    """Simple function to run the scraper and handle execution"""
    try:
        # Import and run the scraper
        from scraper import run_scraper
        result = run_scraper()
        return result
    except KeyboardInterrupt:
        print("\nScraping interrupted by user.")
        return None
    except Exception as e:
        print(f"Error during scraping: {e}")
        import traceback
        traceback.print_exc()
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