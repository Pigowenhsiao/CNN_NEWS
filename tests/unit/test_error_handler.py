"""
Unit tests for error handling functionality
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from src.utils.error_handler import (
    handle_request_failure,
    handle_parsing_failure,
    log_error,
    handle_timeout_error,
    handle_dns_failure,
    safe_request_with_retry
)


def test_handle_request_failure_with_status_404():
    """Test handling of 404 status codes"""
    result = handle_request_failure(404, "https://example.com/nonexistent")
    assert result["status_code"] == 404
    assert "not found" in result["message"].lower()
    assert result["severity"] == "ERROR"


def test_handle_request_failure_with_status_429():
    """Test handling of 429 (rate limit) status codes"""
    result = handle_request_failure(429, "https://example.com/rate-limited")
    assert result["status_code"] == 429
    assert result["severity"] == "WARN"  # Rate limiting is expected behavior


def test_handle_request_failure_with_status_500():
    """Test handling of 500 status codes"""
    result = handle_request_failure(500, "https://example.com/server-error")
    assert result["status_code"] == 500
    assert result["severity"] == "CRITICAL"  # 5xx errors are critical


def test_handle_parsing_failure():
    """Test handling of parsing failures"""
    result = handle_parsing_failure("title", "https://example.com/article", "Missing CSS selector")
    assert result["error_type"] == "PARSING_ERROR"
    assert result["element_type"] == "title"
    assert result["url"] == "https://example.com/article"


def test_handle_timeout_error():
    """Test handling of timeout errors"""
    result = handle_timeout_error("fetch", 10.0, "scraper_module")
    assert result["error_type"] == "TIMEOUT_ERROR"
    assert result["operation"] == "fetch"
    assert result["timeout_duration"] == 10.0
    assert result["severity"] == "WARN"


def test_handle_dns_failure():
    """Test handling of DNS failures"""
    result = handle_dns_failure("example.com", "scraper_module")
    assert result["error_type"] == "DNS_ERROR"
    assert result["domain"] == "example.com"
    assert result["severity"] == "ERROR"


@pytest.mark.asyncio
async def test_safe_request_with_retry_success():
    """Test that safe request with retry works on success"""
    mock_client = AsyncMock()
    mock_response = Mock()
    mock_response.status_code = 200
    mock_client.get.return_value = mock_response
    
    result = await safe_request_with_retry(mock_client, "https://example.com", max_retries=1)
    
    assert result == mock_response
    mock_client.get.assert_called_once_with("https://example.com")


@pytest.mark.asyncio 
async def test_safe_request_with_retry_failure():
    """Test that safe request with retry handles failures"""
    mock_client = AsyncMock()
    mock_client.get.side_effect = Exception("Network error")
    
    result = await safe_request_with_retry(mock_client, "https://example.com", max_retries=2, delay=0.1)
    
    # Result should be None when all retries fail
    assert result is None
    assert mock_client.get.call_count == 2  # Called once initially, then once more after retry


if __name__ == "__main__":
    pytest.main([__file__])