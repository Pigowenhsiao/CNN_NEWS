"""
Date/time parsing and configurable filtering logic for news articles
"""
import sys
from datetime import datetime, timedelta, timezone
from dateutil import parser as dateutil_parser
import re
from pathlib import Path

# Add the src directory to Python path for absolute imports
src_dir = Path(__file__).parent.parent
sys.path.insert(0, str(src_dir))

from models.article import EnhancedNewsArticle
from config.loader import load_config


def is_within_timeframe(pub_date: datetime, hours: int = None) -> bool:
    """
    Check if an article's publication date is within the specified timeframe
    to ensure news relevance as required by constitution principle.
    
    Args:
        pub_date (datetime): The publication date to check
        hours (int, optional): Number of hours for the timeframe. If not provided, uses configured value.
        
    Returns:
        bool: True if date is within the timeframe of current time, False otherwise
    """
    if not pub_date:
        return False
    
    config = load_config()
    max_hours = hours if hours is not None else config['date_filter_hours']
    
    # Ensure both dates are timezone-aware for comparison
    now = datetime.now(timezone.utc)
    if pub_date.tzinfo is None:
        pub_date = pub_date.replace(tzinfo=timezone.utc)
    else:
        pub_date = pub_date.astimezone(timezone.utc)
    
    # Calculate time difference
    time_diff = now - pub_date
    
    # Check if the difference is less than or equal to the specified hours
    max_allowed = timedelta(hours=max_hours)
    return time_diff <= max_allowed


def is_within_72_hours(pub_date: datetime) -> bool:
    """
    Check if an article's publication date is within the last 72 hours (3 days)
    to ensure news relevance as required by constitution principle.
    This function is maintained for backward compatibility.
    
    Args:
        pub_date (datetime): The publication date to check
        
    Returns:
        bool: True if date is within 72 hours of current time, False otherwise
    """
    return is_within_timeframe(pub_date, 72)


def parse_article_date(date_string: str, source: str) -> datetime:
    """
    Parse article publication date from various source-specific formats
    
    Args:
        date_string (str): Raw date string from the article page
        source (str): Source website identifier ("cnn" or "cnbc")
        
    Returns:
        datetime: Parsed datetime object in UTC timezone, or None if parsing fails
    """
    if not date_string:
        return None
    
    try:
        # Different date formats for different sources
        if source.lower() == "cnn":
            # CNN usually has formats like "Published: May 12, 2023" or "Updated May 12, 2023"
            # Remove common prefixes
            cleaned_date = date_string.strip()
            if "updated" in cleaned_date.lower():
                cleaned_date = cleaned_date.lower().replace("updated", "").strip()
            elif "published:" in cleaned_date.lower():
                cleaned_date = cleaned_date.lower().replace("published:", "").strip()
        elif source.lower() == "cnbc":
            # CNBC might have formats like "5:30 PM ET May 12, 2023" or "Published: May 12, 2023 5:30 PM ET"
            cleaned_date = date_string.strip()
            # Remove "Published:" prefix if present
            if "published:" in cleaned_date.lower():
                cleaned_date = cleaned_date.lower().replace("published:", "").strip()
        else:
            # For other sources or if source is unknown, don't modify the date string
            cleaned_date = date_string.strip()
        
        # Use dateutil parser which handles many formats
        parsed_date = dateutil_parser.parse(cleaned_date)
        
        # Ensure the date is timezone-aware (convert to UTC)
        if parsed_date.tzinfo is None:
            parsed_date = parsed_date.replace(tzinfo=timezone.utc)
        else:
            parsed_date = parsed_date.astimezone(timezone.utc)
            
        return parsed_date
    except (ValueError, TypeError):
        # If parsing fails, return None to indicate the failure
        return None


def format_output_date(date_obj: datetime) -> str:
    """
    Format date for output as specified in requirements (YYYY-MM-DD HH:MM:SS format)
    
    Args:
        date_obj (datetime): Date object to format for output
        
    Returns:
        str: Formatted date string in YYYY-MM-DD HH:MM:SS format, or empty string if invalid
    """
    if not date_obj:
        return ""
    
    # Ensure the datetime is in the correct format
    if date_obj.tzinfo is not None:
        # Convert to naive datetime for consistent formatting
        date_obj = date_obj.astimezone(timezone.utc).replace(tzinfo=None)
    
    return date_obj.strftime("%Y-%m-%d %H:%M:%S")


# Example usage
if __name__ == "__main__":
    # Test date parsing with sample formats
    test_dates = [
        ("Published: May 12, 2025", "cnn"),
        ("Updated November 3, 2025", "cnn"),
        ("5:30 PM ET Nov 3, 2025", "cnbc"),
        ("Published: October 31, 2025 10:15 AM EST", "cnbc")
    ]
    
    print("Testing date parsing:")
    for date_str, source in test_dates:
        parsed = parse_article_date(date_str, source)
        if parsed:
            print(f"  {date_str} ({source}) -> {format_output_date(parsed)}")
        else:
            print(f"  {date_str} ({source}) -> FAILED TO PARSE")