"""
News Source model representing the origin of news articles with parsing logic for each source
"""
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class NewsSource:
    """
    Represents the origin of news articles (CNBC Business or CNN Business), 
    with specific parsing logic for each
    """
    name: str  # Name of the source (e.g., "CNN", "CNBC")
    base_url: str  # Base URL for the source
    business_url: str  # Business section URL
    parsing_rules: Dict[str, Any]  # CSS selectors and parsing logic specific to the source
    rate_limit_min: float = 3.0  # Minimum delay between requests in seconds
    rate_limit_max: float = 5.0  # Maximum delay between requests in seconds
    last_accessed: Any = None  # Timestamp of last access for rate limiting