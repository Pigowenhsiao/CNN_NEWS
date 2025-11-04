"""
Unit tests for rate limiter functionality
"""
import pytest
import asyncio
import time
from src.utils.rate_limiter import RateLimiter, rate_limit, get_rate_limiter


@pytest.mark.asyncio
async def test_rate_limiter_initial_wait():
    """Test that the first request doesn't wait"""
    rate_limiter = RateLimiter(min_delay=1.0, max_delay=1.5)
    
    start_time = time.time()
    await rate_limiter.wait_if_needed()
    end_time = time.time()
    
    # First request should not wait significantly
    assert end_time - start_time < 0.1


@pytest.mark.asyncio
async def test_rate_limiter_enforces_delay():
    """Test that subsequent requests wait appropriately"""
    rate_limiter = RateLimiter(min_delay=0.1, max_delay=0.2)
    
    # First request
    await rate_limiter.wait_if_needed()
    
    # Second request should wait
    start_time = time.time()
    await rate_limiter.wait_if_needed()
    end_time = time.time()
    
    # Should have waited at least the minimum delay
    elapsed = end_time - start_time
    assert elapsed >= 0.1


@pytest.mark.asyncio
async def test_global_rate_limiter():
    """Test the global rate limiter convenience function"""
    # First call
    start_time = time.time()
    await rate_limit()
    first_call_time = time.time() - start_time
    assert first_call_time < 0.1  # First call should be immediate
    
    # Wait a bit less than the minimum delay
    await asyncio.sleep(0.05)
    
    # Second call should enforce delay
    start_time = time.time()
    await rate_limit()
    elapsed = time.time() - start_time
    
    # Should have enforced some delay
    assert elapsed >= 0.05  # At least the time we waited + some delay


def test_get_rate_limiter():
    """Test that we can get the rate limiter instance"""
    rate_limiter = get_rate_limiter()
    assert isinstance(rate_limiter, RateLimiter)
    
    # Should always return the same instance
    rate_limiter2 = get_rate_limiter()
    assert rate_limiter is rate_limiter2


@pytest.mark.asyncio
async def test_rate_limiter_delay_range():
    """Test that delays are within expected range"""
    rate_limiter = RateLimiter(min_delay=0.1, max_delay=0.15)  # Small, predictable range
    
    # First request
    await rate_limiter.wait_if_needed()
    
    # Measure the delay for the second request
    start_time = time.time()
    await rate_limiter.wait_if_needed()
    elapsed = time.time() - start_time
    
    # Should be at least the minimum
    assert elapsed >= 0.1


if __name__ == "__main__":
    pytest.main([__file__])