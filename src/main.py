#!/usr/bin/env python3
"""
Main entry point for the Dual Source Financial News Scraper
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Add the src directory to the path so imports work
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.scraper import run_scraper


def main():
    """
    Main entry point for the application
    """
    parser = argparse.ArgumentParser(description="Dual Source Financial News Scraper")
    parser.add_argument("--output", "-o", type=str, help="Output filename for the markdown report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    print("Starting Dual Source Financial News Scraper...")
    print(f"Arguments: output={args.output}, verbose={args.verbose}")
    
    # Run the scraper
    try:
        result = asyncio.run(run_scraper())
        
        if result.articles:
            print(f"Scraping completed successfully!")
            print(f"- Processed {len(result.articles)} articles")
            print(f"- Found {len(result.errors)} errors during scraping")
            
            # Show first few articles if any exist
            if result.articles:
                print("- First few articles:")
                for i, article in enumerate(result.articles[:5]):
                    print(f"  {i+1}. {article.title} [{article.source}]")
        else:
            print("No articles were processed, but the scraper completed run.")
            
        if result.errors:
            print("\nErrors encountered during scraping:")
            for error in result.errors:
                print(f"  - {error['source']}: {error['error']}")
        
        return 0
        
    except KeyboardInterrupt:
        print("\nScraping interrupted by user.")
        return 1
    except Exception as e:
        print(f"Error during scraping: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())