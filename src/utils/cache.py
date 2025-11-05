"""
Caching utilities for avoiding redundant processing of identical articles
"""
import hashlib
from typing import Dict, Optional, Any
from datetime import datetime, timedelta

class ContentCache:
    """
    Simple in-memory cache to store processed content and avoid redundant processing
    """
    def __init__(self, ttl_hours: int = 24):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.ttl_hours = ttl_hours

    def _generate_key(self, url: str, content: str) -> str:
        """
        Generate a unique key for the content based on URL and content hash
        """
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        url_hash = hashlib.sha256(url.encode('utf-8')).hexdigest()
        return f"{url_hash}:{content_hash}"

    def _is_expired(self, timestamp: datetime) -> bool:
        """
        Check if a cached item has expired
        """
        return datetime.now() < timestamp + timedelta(hours=self.ttl_hours)

    def get(self, url: str, content: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached content if available and not expired
        """
        key = self._generate_key(url, content)
        cached_item = self._cache.get(key)
        if cached_item:
            if not self._is_expired(cached_item['timestamp']):
                return cached_item['data']
            else:
                # Remove expired item
                del self._cache[key]
        return None

    def set(self, url: str, content: str, data: Dict[str, Any]) -> None:
        """
        Store processed data in cache
        """
        key = self._generate_key(url, content)
        self._cache[key] = {
            'timestamp': datetime.now(),
            'data': data
        }

    def clear(self) -> None:
        """
        Clear all cached items
        """
        self._cache.clear()

    def cleanup_expired(self) -> None:
        """
        Remove all expired items from cache
        """
        expired_keys = []
        now = datetime.now()
        for key, item in self._cache.items():
            if now >= item['timestamp'] + timedelta(hours=self.ttl_hours):
                expired_keys.append(key)

        for key in expired_keys:
            del self._cache[key]


# Global cache instance
content_cache = ContentCache()