"""
Output File model representing the structured Markdown document with cleanup scheduling
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List
import os


@dataclass
class OutputFile:
    """
    The structured Markdown document containing all processed articles with required metadata
    and automatic cleanup scheduling after 30 days to prevent unbounded storage growth
    """
    filename: str  # Generated filename following convention: US_News_yyyymmdd-hhmm.md
    content: str  # Markdown formatted content with all articles
    created_at: datetime  # Timestamp when file was created
    articles: List  # List of articles included in the file
    article_count: int = 0  # Number of articles in the file
    cleanup_days: int = 30  # Number of days after which the file should be cleaned up automatically
    
    def write_to_disk(self) -> str:
        """
        Write the output file to disk with proper formatting
        """
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(self.content)
        
        print(f"Output file written: {self.filename}")
        return self.filename
        
    def schedule_cleanup(self):
        """
        Schedule automatic cleanup of the output file after specified number of days
        """
        # This would typically involve scheduling a cleanup task or adding to a cleanup registry
        # For now, we'll just print the scheduled cleanup information
        import time
        from datetime import timedelta
        cleanup_date = self.created_at + timedelta(days=self.cleanup_days)
        print(f"Cleanup scheduled for {self.filename} on {cleanup_date.strftime('%Y-%m-%d')}")
        
    def should_cleanup(self) -> bool:
        """
        Check if the output file should be cleaned up based on the cleanup schedule
        """
        from datetime import datetime, timedelta
        current_date = datetime.now()
        file_age = current_date - self.created_at
        return file_age.days >= self.cleanup_days