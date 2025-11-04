"""
Unit tests for performance optimization functionality
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
import asyncio
from src.utils.performance_optimizer import (
    PerformanceOptimizer,
    get_performance_optimizer,
    initialize_connection_pool,
    cache_article_content,
    get_cached_article_content,
    check_memory_usage,
    get_current_performance_metrics
)


def test_performance_optimizer_initialization():
    """Test that PerformanceOptimizer initializes with correct defaults"""
    optimizer = PerformanceOptimizer()
    
    assert optimizer.max_connections == 10
    assert optimizer.max_memory_mb == 500.0
    assert isinstance(optimizer.connection_pool, dict)
    assert isinstance(optimizer.cache, dict)
    assert optimizer.active_requests == 0
    assert optimizer.rate_limit_delays == 0
    assert optimizer.deduplication_savings == 0


def test_estimate_memory_usage():
    """Test memory estimation function"""
    optimizer = PerformanceOptimizer()
    
    # Initially empty cache should have minimal memory usage
    memory_usage = optimizer.estimate_memory_usage()
    assert isinstance(memory_usage, float)
    # Memory usage should be reasonable (not negative, not extremely large for empty cache)
    assert 0 <= memory_usage <= 10.0  # Empty cache should be under 10MB


def test_cache_functionality():
    """Test article content caching functionality"""
    optimizer = PerformanceOptimizer()
    
    # Test caching content
    url = "https://example.com/article1"
    content = {"title": "Test Article", "content": "Test content"}
    
    optimizer.cache_content(url, content)
    
    # Test retrieving cached content
    retrieved_content = optimizer.get_cached_content(url)
    assert retrieved_content == content
    assert url in optimizer.cache
    assert optimizer.cache[url]['access_count'] == 1


def test_cache_ttl_expiry():
    """Test that cached content expires after TTL"""
    optimizer = PerformanceOptimizer()
    
    url = "https://example.com/expired"
    content = "expired content"
    
    # Manually set a cached item with old timestamp
    optimizer.cache[url] = {
        'content': content,
        'timestamp': 0,  # Very old timestamp (1970)
        'access_count': 0
    }
    
    # Retrieving should return None because it's expired
    retrieved_content = optimizer.get_cached_content(url, ttl=1)  # 1 sec TTL
    assert retrieved_content is None
    assert url not in optimizer.cache  # Expired item should be removed


def test_memory_usage_check():
    """Test memory usage check functionality"""
    optimizer = PerformanceOptimizer()
    
    # Should return True with default settings and empty cache
    result = optimizer.is_memory_usage_acceptable()
    assert result is True


@pytest.mark.asyncio
async def test_setup_connection_pool():
    """Test connection pool setup"""
    optimizer = PerformanceOptimizer(max_connections=5)
    
    with patch('httpx.AsyncClient') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        client = await optimizer.setup_connection_pool()
        
        # Verify the client was created with the right parameters
        mock_client_class.assert_called_once()
        args, kwargs = mock_client_class.call_args
        assert kwargs['limits'].max_connections == 5


def test_track_request_time():
    """Test request time tracking"""
    optimizer = PerformanceOptimizer()
    
    # Track a request time
    start_time = 1000.0
    end_time = 1001.5  # 1.5 seconds later
    optimizer.track_request_time(start_time, end_time)
    
    # Verify the time was recorded correctly in ms
    assert len(optimizer.request_times) == 1
    assert optimizer.request_times[0] == 1500.0  # 1.5 seconds = 1500 ms


def test_request_counter():
    """Test active request counter"""
    optimizer = PerformanceOptimizer()
    
    assert optimizer.active_requests == 0
    
    optimizer.increment_active_requests()
    assert optimizer.active_requests == 1
    
    optimizer.increment_active_requests()
    assert optimizer.active_requests == 2
    
    optimizer.decrement_active_requests()
    assert optimizer.active_requests == 1
    
    optimizer.decrement_active_requests()
    assert optimizer.active_requests == 0


def test_global_instance():
    """Test that global instance functions work correctly"""
    # Test getting the global instance
    optimizer = get_performance_optimizer()
    assert isinstance(optimizer, PerformanceOptimizer)
    
    # These functions should use the global instance
    # The functions test basic functionality without throwing errors
    result = check_memory_usage()
    assert isinstance(result, bool)
    

if __name__ == "__main__":
    pytest.main([__file__])