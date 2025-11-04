"""
Utility functions for date/time parsing with comprehensive error handling
"""
from datetime import datetime, timezone, timedelta
from typing import Optional
from dateutil import parser


def parse_article_date(date_string: str, source: str) -> Optional[datetime]:
    """
    Parse publication date from article content according to source-specific formats
    """
    if not date_string:
        return None
        
    try:
        # Handle common date formats from different sources
        if source.lower() == "cnn":
            # CNN often has dates in formats like "Updated: May 12, 2023" or "Updated May 12, 2023"
            date_string = date_string.strip()
            
            # Remove common prefixes
            prefixes = ["Published: ", "Updated: ", "Published ", "Updated "]
            for prefix in prefixes:
                if date_string.startswith(prefix):
                    date_string = date_string[len(prefix):].strip()
                    break
                    
            # Try parsing with dateutil
            return parser.parse(date_string)
        
        elif source.lower() == "cnbc":
            # CNBC might have formats like "5:30 PM EST May 12, 2023" or "May 12, 2023, 5:30 PM"
            date_string = date_string.strip()
            
            # Remove common prefixes
            prefixes = ["Published: ", "First Published: ", "Published ", "First Published "]
            for prefix in prefixes:
                if date_string.startswith(prefix):
                    date_string = date_string[len(prefix):].strip()
                    break
                    
            # Try parsing with dateutil
            return parser.parse(date_string)
        
        # Default: try dateutil parser for unknown sources
        return parser.parse(date_string)
    
    except (ValueError, TypeError, parser.ParserError):
        # If parsing fails, return None to indicate the failure
        return None


def is_within_72_hours(publication_date: datetime) -> bool:
    """
    Check if an article's publication date is within the last 72 hours (3 days)
    """
    if not publication_date:
        return False
        
    # Ensure dates are timezone-aware for comparison
    if publication_date.tzinfo is None:
        publication_date = publication_date.replace(tzinfo=timezone.utc)
    
    now = datetime.now(timezone.utc)
    time_diff = now - publication_date
    
    # Check if the difference is less than or equal to 72 hours
    return time_diff <= timedelta(hours=72)


def format_date_for_output(date_obj: datetime) -> str:
    """
    Format date for output as specified in requirements (YYYY-MM-DD HH:MM:SS format)
    """
    if not date_obj:
        return ""
    
    # Ensure the datetime is in the correct format
    if date_obj.tzinfo is not None:
        # Convert to naive datetime for consistent formatting
        date_obj = date_obj.astimezone(timezone.utc).replace(tzinfo=None)
    
    return date_obj.strftime("%Y-%m-%d %H:%M:%S")


def validate_date_format(date_string: str) -> bool:
    """
    Validate if a date string is in an acceptable format for parsing
    """
    if not date_string:
        return False
    
    try:
        # Try to parse the date string to validate it
        parsed_date = parser.parse(date_string)
        return True
    except (ValueError, TypeError, parser.ParserError):
        return False