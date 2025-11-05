"""
Rate limiting module with configurable delays between requests to avoid being blocked by websites
"""
import asyncio
import random
from datetime import datetime
import sys
from pathlib import Path

# Add the src directory to Python path for absolute imports
src_dir = Path(__file__).parent.parent
sys.path.insert(0, str(src_dir))

from config.loader import load_config


class RateLimiter:
    """
    Implements rate limiting by waiting configurable seconds between each request to avoid being blocked by websites
    """
    
    def __init__(self, min_delay: float = None, max_delay: float = None):
        config = load_config()
        self.min_delay = min_delay if min_delay is not None else config['rate_limit_min_delay']
        self.max_delay = max_delay if max_delay is not None else config['rate_limit_max_delay']
        self.last_request_time = None
        
    async def wait_if_needed(self):
        """
        Wait if needed based on the time of the last request to enforce rate limits
        """
        if self.last_request_time is not None:
            # Calculate elapsed time since last request
            elapsed = datetime.now() - self.last_request_time
            # Generate random delay between min and max
            delay = random.uniform(self.min_delay, self.max_delay)
            
            # If less time has passed than required delay, wait for remainder
            if elapsed.total_seconds() < delay:
                remaining = delay - elapsed.total_seconds()
                await asyncio.sleep(remaining)
        
        # Update the last request time
        self.last_request_time = datetime.now()


# Create default rate limiter instance
default_rate_limiter = RateLimiter()


async def rate_limit():
    """
    Convenience function to apply rate limiting between requests
    """
    await default_rate_limiter.wait_if_needed()


def get_rate_limiter() -> RateLimiter:
    """
    Get the default rate limiter instance
    """
    return default_rate_limiter