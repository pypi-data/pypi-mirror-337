"""
Scalability components for handling large-scale knowledge graphs.

This module provides functionality for managing large-scale knowledge graphs,
including summarization and caching mechanisms.
"""

from synapsegraph_lib.scalability.summarization import SummarizationManager
from synapsegraph_lib.scalability.caching import CacheManager

__all__ = ["SummarizationManager", "CacheManager"]
