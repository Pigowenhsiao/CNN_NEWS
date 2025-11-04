"""
Unit tests for data integrity validation
"""
import pytest
from datetime import datetime
from src.models.article import NewsArticle
from src.models.result import ScrapeResult


def test_news_article_required_fields():
    """Test that NewsArticle has all required fields"""
    article = NewsArticle(
        id="test-id",
        title="Test Title",
        content="Test content",
        url="http://example.com",
        publication_date=datetime.now(),
        source="Test Source"
    )
    
    assert hasattr(article, 'id')
    assert hasattr(article, 'title')
    assert hasattr(article, 'content')
    assert hasattr(article, 'url')
    assert hasattr(article, 'publication_date')
    assert hasattr(article, 'source')
    assert hasattr(article, 'scraped_at')
    assert hasattr(article, 'status')
    
    assert article.id == "test-id"
    assert article.title == "Test Title"
    assert article.content == "Test content"
    assert article.url == "http://example.com"
    assert article.source == "Test Source"
    assert article.status == "pending"


def test_news_article_field_types():
    """Test that NewsArticle fields have correct types"""
    pub_date = datetime.now()
    article = NewsArticle(
        id="test-id",
        title="Test Title",
        content="Test content",
        url="http://example.com",
        publication_date=pub_date,
        source="Test Source"
    )
    
    assert isinstance(article.id, str)
    assert isinstance(article.title, str)
    assert isinstance(article.content, str)
    assert isinstance(article.url, str)
    assert isinstance(article.publication_date, datetime)
    assert isinstance(article.source, str)
    assert isinstance(article.status, str)


def test_scrape_result_structure():
    """Test that ScrapeResult has correct structure"""
    result = ScrapeResult(
        articles=[],
        errors=[]
    )
    
    assert hasattr(result, 'articles')
    assert hasattr(result, 'errors')
    assert hasattr(result, 'start_time')
    assert hasattr(result, 'end_time')
    assert hasattr(result, 'source_stats')
    
    assert result.articles == []
    assert result.errors == []


def test_data_integrity_validation():
    """Test comprehensive data integrity validation"""
    # Create a valid article
    valid_article = NewsArticle(
        id="valid-id",
        title="Valid Title",
        content="Valid content",
        url="https://example.com",
        publication_date=datetime.now(),
        source="Valid Source"
    )
    
    # Validate required fields are not empty
    assert valid_article.id.strip() != ""
    assert valid_article.title.strip() != ""
    assert valid_article.content.strip() != ""
    assert valid_article.url.strip() != ""
    assert valid_article.source.strip() != ""
    
    # Validate URL format (basic check)
    assert "http" in valid_article.url.lower()


if __name__ == "__main__":
    pytest.main([__file__])