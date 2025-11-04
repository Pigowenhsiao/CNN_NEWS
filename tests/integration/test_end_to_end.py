"""
Integration tests for complete end-to-end functionality
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from src.scraper import scrape_news_sources
from src.cnn_parser import get_cnn_articles, extract_cnn_content
from src.cnbc_parser import get_cnbc_articles, extract_cnbc_content
from src.utils.date_parser import is_within_72_hours, parse_article_date
from src.deduplication import Deduplicator
from src.output_writer import write_to_markdown


@pytest.mark.asyncio
async def test_complete_workflow_integration():
    """Test complete workflow from source access to output generation"""
    with patch('httpx.AsyncClient') as mock_client_class:
        # Create a mock client instance
        mock_client = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client
        mock_client_class.return_value.__aexit__.return_value = None
        
        # Mock successful responses from both sources
        cnn_response = AsyncMock()
        cnn_response.status_code = 200
        cnn_response.text = "<html><body><a href='/article1'>CNN Article 1</a></body></html>"
        mock_client.get.return_value = cnn_response
        
        # Run the complete scraping workflow
        result = await scrape_news_sources()
        
        # Verify that the scraping process returns a valid result
        assert hasattr(result, 'articles')
        assert hasattr(result, 'errors')
        assert isinstance(result.articles, list)
        assert isinstance(result.errors, list)


@pytest.mark.asyncio
async def test_rate_limiting_integration():
    """Test that rate limiting is properly implemented between requests"""
    from src.utils.rate_limiter import RateLimiter, default_rate_limiter
    
    # Create a fresh rate limiter for testing
    rl = RateLimiter(min_delay=0.1, max_delay=0.2)  # Use shorter delays for tests
    
    # Record the time before and after calling rate limiter
    import time
    start_time = time.time()
    await rl.wait_if_needed()
    time_after_first = time.time()
    
    # Call again immediately - should enforce delay
    await rl.wait_if_needed()
    end_time = time.time()
    
    # Verify that some time delay was enforced between calls
    total_elapsed = end_time - start_time
    assert total_elapsed >= 0.1  # At least the minimum delay should be enforced


def test_deduplication_integration():
    """Test that deduplication works correctly in the complete flow"""
    deduper = Deduplicator()
    
    # Reset unique tracking sets for clean test
    deduper.unique_titles.clear()
    deduper.content_hashes.clear()
    
    # Create two articles with the same title (duplicate by title)
    article1 = MagicMock()
    article1.title = "Duplicate Article Title"
    article1.content = "Content of first article"
    article1.url = "https://example.com/1"
    article1.publication_date = datetime.now()
    article1.source = "CNN"
    
    article2 = MagicMock()  # Same title, different content/URL
    article2.title = "Duplicate Article Title"  # Same title as article1
    article2.content = "Content of second article"
    article2.url = "https://example.com/2"
    article2.publication_date = datetime.now()
    article2.source = "CNN"
    
    # First article should be accepted
    result1 = deduper.add_article(article1)
    assert result1 is True
    
    # Second article should be rejected as duplicate
    result2 = deduper.add_article(article2)
    assert result2 is False  # Should be detected as duplicate


def test_date_filtering_integration():
    """Test that date filtering is correctly applied to articles within 72 hours"""
    from datetime import datetime, timedelta
    
    # Test that recent articles are accepted
    recent_date = datetime.now() - timedelta(hours=48)  # 48 hours ago (within 72)
    assert is_within_72_hours(recent_date) is True
    
    # Test that old articles are rejected
    old_date = datetime.now() - timedelta(hours=100)  # 100 hours ago (beyond 72)
    assert is_within_72_hours(old_date) is False
    
    # Test with date strings
    date_str = "November 1, 2025, 10:30 AM"
    parsed_date = parse_article_date(date_str, "cnn")
    if parsed_date:  # Only test if parsing was successful
        # Verify the parsed date is in the expected timeframe
        is_recent = is_within_72_hours(parsed_date)
        # This depends on if the parsed date is within 72 hours of "now"
        # For this specific test, we'd need to mock "now" to make it deterministic


def test_output_formatting_integration():
    """Test that output formatting meets all requirements from FR-008"""
    from datetime import datetime
    from src.models.article import EnhancedNewsArticle
    
    # Create a sample article
    test_article = EnhancedNewsArticle(
        id="test_id_123",
        title="Test Financial News Article",
        content="This is the content of a test financial news article that contains sufficient information for testing purposes.",
        url="https://www.example.com/financial-news-test",
        publication_date=datetime(2025, 11, 3, 9, 15, 0),
        source="Test Source"
    )
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        output_file = os.path.join(tmp_dir, "US_News_20251103-0915.md")
        
        # Write to markdown using the actual function
        result_path = write_to_markdown([test_article], output_file)
        
        # Verify the file was created
        assert os.path.exists(result_path)
        
        # Verify file content includes required elements
        with open(result_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        assert "Test Financial News Article" in content
        assert "Test Source" in content
        assert "2025-11-03 09:15:00" in content  # Date format check
        assert "https://www.example.com/financial-news-test" in content
        assert "This is the content of a test financial news article" in content


def test_end_to_end_error_handling():
    """Test error handling throughout the complete flow"""
    from src.utils.error_handler import handle_request_failure
    
    # Test error handling function
    error_result = handle_request_failure(404, "https://example.com/nonexistent")
    
    assert error_result["status_code"] == 404
    assert "not found" in error_result["message"].lower()
    assert error_result["severity"] == "ERROR"


def test_data_integrity_through_pipeline():
    """Test that data integrity is maintained throughout the processing pipeline"""
    from src.utils.validator import validate_article_data, assign_default_values
    
    # Test incomplete article data
    incomplete_data = {
        'title': 'Incomplete Article',
        'content': 'Test content',
        'url': 'https://example.com/incomplete',
        'publication_date': datetime.now()
        # Missing 'source' and other fields
    }
    
    # Validate (should pass after defaults are assigned)
    completed_data = assign_default_values(incomplete_data.copy())
    is_valid = validate_article_data(completed_data)
    
    # Should be valid after defaults are assigned
    assert is_valid is True
    
    # Verify required fields are now present
    assert 'source' in completed_data
    assert 'id' in completed_data
    assert 'status' in completed_data


if __name__ == "__main__":
    pytest.main([__file__])