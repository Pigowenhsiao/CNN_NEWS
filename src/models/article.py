"""
Enhanced News Article model with additional validation fields and quality metrics
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class EnhancedNewsArticle:
    """
    Represents an individual news piece with id, title, content, URL, 
    publication date, and source website. Includes validation fields and quality metrics.
    """
    id: str
    title: str
    content: str
    url: str
    publication_date: datetime
    source: str
    scraped_at: Optional[datetime] = None
    status: str = "pending"  # pending, processed, filtered, failed
    quality_score: float = 0.0  # 0.0-1.0 automated quality assessment
    similarity_hash: Optional[str] = None  # Content hash for duplicate detection
    processing_time_ms: Optional[int] = None  # Processing time in milliseconds