"""
Scraping Result model containing collected data from the scraping process along with errors and statistics
"""
from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime
import time
from .article import EnhancedNewsArticle


@dataclass
class ScrapingResult:
    """
    Contains the collected data from the scraping process, including successfully processed articles and any errors encountered,
    with execution statistics
    """
    articles: List[EnhancedNewsArticle]  # List of successfully processed articles
    errors: List[Dict[str, Any]]  # List of error dictionaries with details
    start_time: float  # Start time of scraping process (timestamp)
    end_time: float  # End time of scraping process (timestamp)
    duration_seconds: float  # Total duration of scraping in seconds
    source_stats: Dict[str, Any] = None  # Statistics per source (e.g., count of articles, success rate)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get execution statistics for the scraping run
        """
        if self.source_stats is None:
            # Calculate basic statistics if not provided
            self.source_stats = {}
            for article in self.articles:
                source = article.source
                if source in self.source_stats:
                    self.source_stats[source]['count'] += 1
                else:
                    self.source_stats[source] = {'count': 1}
        
        return {
            "total_articles": len(self.articles),
            "total_errors": len(self.errors),
            "duration_seconds": self.duration_seconds,
            "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
            "end_time": datetime.fromtimestamp(self.end_time).isoformat(),
            "source_stats": self.source_stats
        }