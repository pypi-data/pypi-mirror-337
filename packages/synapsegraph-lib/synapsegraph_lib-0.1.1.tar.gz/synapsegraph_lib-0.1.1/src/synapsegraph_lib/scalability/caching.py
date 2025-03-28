"""
Caching module for SynapseGraph.

This module provides caching mechanisms for improving performance of the knowledge graph,
including query result caching and frequently accessed node caching.
"""

import logging
from typing import Dict, Any, Optional, Callable, Tuple, List
from datetime import datetime, timedelta
import functools
import hashlib
import json

logger = logging.getLogger(__name__)


class CacheManager:
    """
    Manages caching for the knowledge graph.

    This class is responsible for:
    1. Caching query results
    2. Caching frequently accessed nodes
    3. Managing cache invalidation
    """

    def __init__(self, cache_ttl_seconds: int = 3600):
        """
        Initialize the CacheManager.

        Args:
            cache_ttl_seconds: Time-to-live for cached items in seconds
        """
        self.cache: Dict[str, Tuple[Any, datetime]] = {}
        self.cache_ttl = timedelta(seconds=cache_ttl_seconds)

    def cache_query(self, func: Callable) -> Callable:
        """
        Decorator for caching query results.

        Args:
            func: The function to cache results for

        Returns:
            Decorated function with caching
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create a cache key from the function name and arguments
            key_parts = [func.__name__]
            key_parts.extend([str(arg) for arg in args])
            key_parts.extend([f"{k}={v}" for k, v in sorted(kwargs.items())])
            key = hashlib.md5(json.dumps(key_parts).encode()).hexdigest()

            # Check if result is in cache and not expired
            if key in self.cache:
                result, timestamp = self.cache[key]
                if datetime.now() - timestamp < self.cache_ttl:
                    logger.debug(f"Cache hit for {func.__name__}")
                    return result

            # Execute function and cache result
            result = func(*args, **kwargs)
            self.cache[key] = (result, datetime.now())
            logger.debug(f"Cache miss for {func.__name__}, result cached")
            return result

        return wrapper

    def invalidate_cache(self, pattern: Optional[str] = None) -> int:
        """
        Invalidate cache entries.

        Args:
            pattern: Optional pattern to match cache keys for selective invalidation

        Returns:
            Number of invalidated cache entries
        """
        if pattern is None:
            count = len(self.cache)
            self.cache.clear()
            logger.info(f"Invalidated {count} cache entries")
            return count

        keys_to_remove = [k for k in self.cache.keys() if pattern in k]
        for key in keys_to_remove:
            del self.cache[key]

        logger.info(
            f"Invalidated {len(keys_to_remove)} cache entries matching '{pattern}'"
        )
        return len(keys_to_remove)

    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the cache.

        Returns:
            Dictionary with cache statistics
        """
        current_time = datetime.now()
        total_entries = len(self.cache)
        expired_entries = sum(
            1
            for _, timestamp in self.cache.values()
            if current_time - timestamp >= self.cache_ttl
        )

        return {
            "total_entries": total_entries,
            "active_entries": total_entries - expired_entries,
            "expired_entries": expired_entries,
            "cache_ttl_seconds": self.cache_ttl.total_seconds(),
        }
