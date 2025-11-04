"""
Performance Metrics model for tracking execution time, memory usage, and throughput
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class PerformanceMetrics:
    """
    Execution time, memory usage, throughput statistics, and other metrics 
    for optimization tracking
    """
    collection_time: datetime  # When metrics were recorded
    execution_time_ms: Optional[int]  # Total execution time in milliseconds
    memory_usage_mb: Optional[float]  # Current memory usage in MB
    peak_memory_mb: Optional[float]  # Peak memory usage in MB
    articles_per_second: Optional[float]  # Throughput rate
    network_requests: Optional[int]  # Total number of network requests made
    successful_requests: Optional[int]  # Number of successful network requests
    failed_requests: Optional[int]  # Number of failed network requests
    average_request_time_ms: Optional[float]  # Average network request time
    cpu_usage_percent: Optional[float]  # CPU usage percentage during execution
    connection_pool_size: Optional[int]  # Size of HTTP connection pool
    cache_hit_rate: Optional[float]  # Percentage of cache hits (0.0-1.0)
    active_coroutines: Optional[int]  # Number of active async coroutines
    rate_limit_delays: Optional[int]  # Number of rate limiting delays applied
    deduplication_savings: Optional[int]  # Number of articles not processed due to deduplication