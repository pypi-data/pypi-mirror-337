"""
Retrieval module for accessing knowledge from SynapseGraph.

This module provides clean, intuitive methods to retrieve knowledge
from the SynapseGraph knowledge base.
"""

import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

from synapsegraph_lib.core.models import Entity, Belief, Opinion, Neo4jConnection
from synapsegraph_lib.core.config import OpinionStance, TimeHorizon

logger = logging.getLogger(__name__)


class KnowledgeRetrieval:
    """
    Provides clean, intuitive methods to retrieve knowledge from SynapseGraph.
    """

    def __init__(self, db: Neo4jConnection):
        """
        Initialize the knowledge retrieval system.

        Args:
            db: Neo4j database connection
        """
        self.db = db

    def get_by_topic(self, topic: str, limit: int = 10) -> Dict:
        """
        Get beliefs and opinions related to a topic.

        Args:
            topic: The topic to search for
            limit: Maximum number of results to return

        Returns:
            Dictionary containing beliefs and opinions
        """
        query = """
        MATCH (b:Belief)
        WHERE b.topic = $topic
        RETURN b
        ORDER BY b.confidence DESC
        LIMIT $limit
        """

        beliefs = self.db.execute_query(
            query, {"topic": topic, "limit": limit}, fetch_all=True
        )

        query = """
        MATCH (o:Opinion)
        WHERE o.topic = $topic
        RETURN o
        ORDER BY o.confidence DESC
        LIMIT $limit
        """

        opinions = self.db.execute_query(
            query, {"topic": topic, "limit": limit}, fetch_all=True
        )

        return {
            "beliefs": [Belief.from_dict(b["b"]) for b in beliefs],
            "opinions": [Opinion.from_dict(o["o"]) for o in opinions],
        }

    def get_by_entity(self, entity_name: str) -> Dict:
        """
        Get all knowledge related to an entity.

        Args:
            entity_name: Name of the entity

        Returns:
            Dictionary containing entity and related knowledge
        """
        # Get entity
        query = """
        MATCH (e:Entity {name: $name})
        RETURN e
        """
        entity_result = self.db.execute_query(
            query, {"name": entity_name}, fetch_all=True
        )
        entity = Entity.from_dict(entity_result[0]["e"]) if entity_result else None

        # Get related beliefs
        query = """
        MATCH (e:Entity {name: $name})<-[:BELIEVED_BY]-(b:Belief)
        RETURN b
        ORDER BY b.confidence DESC
        """
        beliefs = self.db.execute_query(query, {"name": entity_name}, fetch_all=True)

        # Get related opinions
        query = """
        MATCH (e:Entity {name: $name})<-[:OPINION_ABOUT]-(o:Opinion)
        RETURN o
        ORDER BY o.confidence DESC
        """
        opinions = self.db.execute_query(query, {"name": entity_name}, fetch_all=True)

        return {
            "entity": entity,
            "beliefs": [Belief.from_dict(b["b"]) for b in beliefs],
            "opinions": [Opinion.from_dict(o["o"]) for o in opinions],
        }

    def semantic_search(self, query: str, limit: int = 10) -> Dict:
        """
        Search knowledge by semantic similarity.

        Args:
            query: The search query
            limit: Maximum number of results to return

        Returns:
            Dictionary containing matching beliefs, opinions, and entities
        """
        # Search beliefs
        belief_query = """
        MATCH (b:Belief)
        WHERE b.statement CONTAINS $query
        RETURN b
        ORDER BY b.confidence DESC
        LIMIT $limit
        """
        beliefs = self.db.execute_query(
            belief_query, {"query": query, "limit": limit}, fetch_all=True
        )

        # Search opinions
        opinion_query = """
        MATCH (o:Opinion)
        WHERE o.statement CONTAINS $query
        RETURN o
        ORDER BY o.confidence DESC
        LIMIT $limit
        """
        opinions = self.db.execute_query(
            opinion_query, {"query": query, "limit": limit}, fetch_all=True
        )

        # Search entities
        entity_query = """
        MATCH (e:Entity)
        WHERE e.name CONTAINS $query OR e.description CONTAINS $query
        RETURN e
        LIMIT $limit
        """
        entities = self.db.execute_query(
            entity_query, {"query": query, "limit": limit}, fetch_all=True
        )

        return {
            "beliefs": [Belief.from_dict(b["b"]) for b in beliefs],
            "opinions": [Opinion.from_dict(o["o"]) for o in opinions],
            "entities": [Entity.from_dict(e["e"]) for e in entities],
        }

    def get_by_confidence(self, min_confidence: float = 0.7) -> Dict:
        """
        Get high-confidence knowledge.

        Args:
            min_confidence: Minimum confidence threshold

        Returns:
            Dictionary containing high-confidence beliefs and opinions
        """
        # Get high-confidence beliefs
        belief_query = """
        MATCH (b:Belief)
        WHERE b.confidence >= $min_confidence
        RETURN b
        ORDER BY b.confidence DESC
        """
        beliefs = self.db.execute_query(
            belief_query, {"min_confidence": min_confidence}, fetch_all=True
        )

        # Get high-confidence opinions
        opinion_query = """
        MATCH (o:Opinion)
        WHERE o.confidence >= $min_confidence
        RETURN o
        ORDER BY o.confidence DESC
        """
        opinions = self.db.execute_query(
            opinion_query, {"min_confidence": min_confidence}, fetch_all=True
        )

        return {
            "beliefs": [Belief.from_dict(b["b"]) for b in beliefs],
            "opinions": [Opinion.from_dict(o["o"]) for o in opinions],
        }

    def get_by_timeframe(self, start_time: datetime, end_time: datetime) -> Dict:
        """
        Get knowledge within a specific timeframe.

        Args:
            start_time: Start of the timeframe
            end_time: End of the timeframe

        Returns:
            Dictionary containing beliefs and opinions within the timeframe
        """
        # Get beliefs in timeframe
        belief_query = """
        MATCH (b:Belief)
        WHERE b.created_at >= datetime($start_time) 
        AND b.created_at <= datetime($end_time)
        RETURN b
        ORDER BY b.created_at DESC
        """
        beliefs = self.db.execute_query(
            belief_query,
            {"start_time": start_time.isoformat(), "end_time": end_time.isoformat()},
            fetch_all=True,
        )

        # Get opinions in timeframe
        opinion_query = """
        MATCH (o:Opinion)
        WHERE o.created_at >= datetime($start_time) 
        AND o.created_at <= datetime($end_time)
        RETURN o
        ORDER BY o.created_at DESC
        """
        opinions = self.db.execute_query(
            opinion_query,
            {"start_time": start_time.isoformat(), "end_time": end_time.isoformat()},
            fetch_all=True,
        )

        return {
            "beliefs": [Belief.from_dict(b["b"]) for b in beliefs],
            "opinions": [Opinion.from_dict(o["o"]) for o in opinions],
        }
