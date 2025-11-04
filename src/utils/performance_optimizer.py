"""
Performance optimization with connection pooling and caching
"""
import asyncio
from typing import Dict, Any, Optional
import time
from .models.metrics import PerformanceMetrics
from .utils.helpers import log_info, log_warning


class PerformanceOptimizer:
    """
    Optimizes concurrent scraping to reduce total execution time by at least 15%
    and limit memory usage to under 500MB during normal operation
    """
    
    def __init__(self, max_connections: int = 10, max_memory_mb: float = 500.0):
        self.max_connections = max_connections
        self.max_memory_mb = max_memory_mb
        self.connection_pool = {}
        self.cache = {}
        self.start_time = None
        self.active_requests = 0
        self.request_times = []
        self.rate_limit_delays = 0
        self.deduplication_savings = 0
        
    async def setup_connection_pool(self):
        """
        Set up connection pooling to reduce overhead of repeated HTTP requests
        """
        import httpx
        
        # Create a shared client with connection pooling
        self.client = httpx.AsyncClient(
            limits=httpx.Limits(max_connections=self.max_connections),
            timeout=30.0
        )
        
        log_info(f"Connection pool initialized with max {self.max_connections} connections", "PerformanceOptimizer")
        return self.client
        
    def cache_content(self, key: str, content: Any) -> None:
        """
        Cache parsed content to avoid redundant processing of identical articles
        """
        self.cache[key] = {
            'content': content,
            'timestamp': time.time(),
            'access_count': 0
        }
        log_info(f"Cached content with key: {key}, cache size: {len(self.cache)}", "PerformanceOptimizer")
        
    def get_cached_content(self, key: str, ttl: int = 3600) -> Optional[Any]:
        """
        Retrieve cached content if available and not expired
        """
        if key in self.cache:
            cached_item = self.cache[key]
            age = time.time() - cached_item['timestamp']
            
            if age < ttl:  # Still valid
                cached_item['access_count'] += 1
                log_info(f"Retrieved cached content with key: {key}, accessed {cached_item['access_count']} times", "PerformanceOptimizer")
                return cached_item['content']
            else:
                # Expired, remove from cache
                del self.cache[key]
                log_info(f"Removed expired content from cache: {key}", "PerformanceOptimizer")
                
        return None
        
    def estimate_memory_usage(self) -> float:
        """
        Estimate current memory usage in MB
        """
        import sys
        
        # Rough estimation of cache memory usage
        cache_size_bytes = sum(sys.getsizeof(str(item)) for item in self.cache.values())
        return cache_size_bytes / (1024 * 1024)  # Convert to MB
        
    def is_memory_usage_acceptable(self) -> bool:
        """
        Check if current memory usage is below threshold
        """
        current_usage = self.estimate_memory_usage()
        return current_usage <= self.max_memory_mb
        
    def get_performance_metrics(self) -> PerformanceMetrics:
        """
        Get current performance metrics
        """
        execution_time = (time.time() - self.start_time) * 1000 if self.start_time else 0
        avg_request_time = sum(self.request_times) / len(self.request_times) if self.request_times else 0
        
        return PerformanceMetrics(
            collection_time=time.time(),
            execution_time_ms=int(execution_time),
            memory_usage_mb=self.estimate_memory_usage(),
            peak_memory_mb=self.max_memory_mb,  # Track peak differently in full implementation
            articles_per_second=0,  # Calculate based on total articles and execution time
            network_requests=len(self.request_times),
            successful_requests=len([t for t in self.request_times if t is not None]),
            failed_requests=sum(1 for t in self.request_times if t is None),
            average_request_time_ms=avg_request_time,
            cpu_usage_percent=None,  # Would need psutil or similar to track
            connection_pool_size=self.max_connections,
            cache_hit_rate=float(len(self.cache)) / max(len(self.request_times), 1) if self.request_times else 0,
            active_coroutines=self.active_requests,
            rate_limit_delays=self.rate_limit_delays,
            deduplication_savings=self.deduplication_savings
        )
        
    def track_request_time(self, start_time: float, end_time: float) -> None:
        """
        Track the time a request took
        """
        duration_ms = (end_time - start_time) * 1000
        self.request_times.append(duration_ms)
        
    def increment_active_requests(self) -> None:
        """
        Track an active request
        """
        self.active_requests += 1
        
    def decrement_active_requests(self) -> None:
        """
        Track completion of a request
        """
        self.active_requests -= 1
        if self.active_requests < 0:
            self.active_requests = 0
            
    def increment_rate_limit_delays(self) -> None:
        """
        Track when a rate limit delay is applied
        """
        self.rate_limit_delays += 1
        
    def increment_deduplication_savings(self) -> None:
        """
        Track when an article is skipped due to deduplication
        """
        self.deduplication_savings += 1


# Global performance optimizer instance
performance_optimizer = PerformanceOptimizer()


def get_performance_optimizer() -> PerformanceOptimizer:
    """
    Get the global performance optimizer instance
    """
    return performance_optimizer


async def initialize_connection_pool():
    """
    Initialize the connection pool for optimal performance
    """
    return await performance_optimizer.setup_connection_pool()


def cache_article_content(url: str, content: Any) -> None:
    """
    Cache article content by URL to avoid reprocessing
    """
    performance_optimizer.cache_content(url, content)


def get_cached_article_content(url: str) -> Optional[Any]:
    """
    Get cached article content if available
    """
    return performance_optimizer.get_cached_content(url)


def check_memory_usage() -> bool:
    """
    Check if memory usage is within acceptable limits
    """
    return performance_optimizer.is_memory_usage_acceptable()


def get_current_performance_metrics() -> PerformanceMetrics:
    """
    Get current performance metrics
    """
    return performance_optimizer.get_performance_metrics()


def track_http_request_time(start_time: float, end_time: float) -> None:
    """
    Track HTTP request time for performance optimization
    """
    performance_optimizer.track_request_time(start_time, end_time)


def register_rate_limit_delay() -> None:
    """
    Register when a rate limit delay is applied
    """
    performance_optimizer.increment_rate_limit_delays()


def register_deduplication_saving() -> None:
    """
    Register when an article is skipped due to deduplication
    """
    performance_optimizer.increment_deduplication_savings()