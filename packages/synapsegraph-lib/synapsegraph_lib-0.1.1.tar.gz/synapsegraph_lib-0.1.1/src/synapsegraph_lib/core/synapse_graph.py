"""
Main SynapseGraph class that provides the primary interface for interacting with the knowledge graph.

This module integrates all components of the SynapseGraph system and provides a clean,
intuitive interface for knowledge retrieval and management.
"""

import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

from synapsegraph_lib.core.models import Entity, Belief, Opinion
from synapsegraph_lib.core.database import Neo4jConnection
from synapsegraph_lib.core.config import OpinionStance, TimeHorizon, ConflictStatus
from synapsegraph_lib.core.retrieval import KnowledgeRetrieval
from synapsegraph_lib.synthesis.opinion_formation import OpinionSynthesizer
from synapsegraph_lib.synthesis.belief_manager import BeliefManager
from synapsegraph_lib.integrity.conflict_resolution import ConflictManager
from synapsegraph_lib.temporal.temporal_management import TemporalManager
from synapsegraph_lib.integrity.balance_monitoring import BalanceMonitor
from synapsegraph_lib.integrity.conflict_resolution_llm import ConflictAnalysis

logger = logging.getLogger(__name__)


class SynapseGraph:
    """
    Main interface for interacting with the SynapseGraph knowledge graph system.

    This class integrates all components of the system and provides a clean,
    intuitive interface for knowledge retrieval and management.
    """

    def __init__(self, db: Neo4jConnection):
        """
        Initialize the SynapseGraph system.

        Args:
            db: Neo4j database connection
        """
        self.db = db

        # Initialize components
        self.retrieval = KnowledgeRetrieval(db)
        self.temporal_manager = TemporalManager()
        self.opinion_synthesizer = OpinionSynthesizer(self.temporal_manager)
        self.belief_manager = BeliefManager(db)
        self.conflict_manager = ConflictManager(self.opinion_synthesizer)
        self.balance_monitor = BalanceMonitor()

        # Create database constraints
        self.db.create_constraints()

    def get_knowledge_by_topic(self, topic: str, limit: int = 10) -> Dict:
        """
        Get beliefs and opinions related to a topic.

        Args:
            topic: The topic to search for
            limit: Maximum number of results to return

        Returns:
            Dictionary containing beliefs and opinions
        """
        return self.retrieval.get_by_topic(topic, limit)

    def get_knowledge_by_entity(self, entity_name: str) -> Dict:
        """
        Get all knowledge related to an entity.

        Args:
            entity_name: Name of the entity

        Returns:
            Dictionary containing entity and related knowledge
        """
        return self.retrieval.get_by_entity(entity_name)

    def search_knowledge(self, query: str, limit: int = 10) -> Dict:
        """
        Search knowledge by semantic similarity.

        Args:
            query: The search query
            limit: Maximum number of results to return

        Returns:
            Dictionary containing matching beliefs, opinions, and entities
        """
        return self.retrieval.semantic_search(query, limit)

    def get_high_confidence_knowledge(self, min_confidence: float = 0.7) -> Dict:
        """
        Get high-confidence knowledge.

        Args:
            min_confidence: Minimum confidence threshold

        Returns:
            Dictionary containing high-confidence beliefs and opinions
        """
        return self.retrieval.get_by_confidence(min_confidence)

    def get_knowledge_by_timeframe(
        self, start_time: datetime, end_time: datetime
    ) -> Dict:
        """
        Get knowledge within a specific timeframe.

        Args:
            start_time: Start of the timeframe
            end_time: End of the timeframe

        Returns:
            Dictionary containing beliefs and opinions within the timeframe
        """
        return self.retrieval.get_by_timeframe(start_time, end_time)

    def synthesize_opinion(
        self, topic: str, min_confidence: float = 0.3
    ) -> Optional[Opinion]:
        """
        Synthesize an opinion from beliefs related to a topic.

        Args:
            topic: Topic to synthesize an opinion for
            min_confidence: Minimum confidence threshold for beliefs

        Returns:
            Opinion object if successful, None otherwise
        """
        return self.opinion_synthesizer.synthesize_opinion(
            self.db, topic, min_confidence
        )

    def update_opinion(
        self,
        existing_opinion: Opinion,
        new_beliefs: List[Belief],
        updated_by: str = "system",
        domain_context: str = None,
    ) -> Optional[Opinion]:
        """
        Update an existing opinion based on new beliefs.

        Args:
            existing_opinion: Existing Opinion object
            new_beliefs: List of new Belief objects
            updated_by: Identifier of who/what is updating the opinion
            domain_context: Domain context for adaptive resistance calculation

        Returns:
            Updated Opinion object if successful, None otherwise
        """
        return self.opinion_synthesizer.update_opinion(
            self.db, existing_opinion, new_beliefs, updated_by, domain_context
        )

    def check_opinion_balance(self, topic: str) -> Dict:
        """
        Check the balance of opinions on a topic.

        Args:
            topic: Topic to check balance for

        Returns:
            Dictionary containing balance metrics and recommendations
        """
        return self.balance_monitor.check_balance(self.db, topic)

    def apply_temporal_decay(self, days: int = 30) -> Dict:
        """
        Apply temporal decay to beliefs and opinions.

        Args:
            days: Number of days to simulate

        Returns:
            Dictionary containing decay statistics
        """
        return self.temporal_manager.apply_decay(self.db, days)

    def resolve_conflicts(self, topic: str) -> Dict[str, Any]:
        """
        Resolve conflicts for a given topic.

        Args:
            topic: Topic to resolve conflicts for

        Returns:
            Dict containing resolution status and details
        """
        try:
            # Get active conflicts for the topic
            conflicts = self.conflict_manager.get_conflicts_for_topic(self.db, topic)

            if not conflicts:
                return {
                    "status": "success",
                    "message": f"No active conflicts found for topic '{topic}'",
                    "resolved_conflicts": [],
                }

            resolved_conflicts = []
            for conflict in conflicts:
                resolved = self.conflict_manager.resolve_conflict(self.db, conflict)
                if resolved:
                    resolved_conflicts.append(resolved)

            return {
                "status": "success",
                "message": f"Successfully resolved {len(resolved_conflicts)} conflicts",
                "resolved_conflicts": resolved_conflicts,
            }

        except Exception as e:
            logging.error(f"Error resolving conflicts: {str(e)}")
            return {"status": "error", "message": str(e)}

    def get_conflict_analysis(self, topic: str) -> List[Dict[str, Any]]:
        """
        Get detailed analysis of conflicts for a topic.

        Args:
            topic: Topic to analyze conflicts for

        Returns:
            List of conflict analysis results
        """
        try:
            # Find conflicts for the topic
            query = """
            MATCH (cr:ConflictResolution)
            WHERE toLower(cr.topic) CONTAINS toLower($topic)
            MATCH (cr)<-[:PART_OF_CONFLICT]-(o:Opinion)
            RETURN cr, collect(o) as opinions
            """
            results = self.db.execute_query(query, {"topic": topic}, fetch_all=True)

            analyses = []
            for result in results:
                if "cr" not in result or "opinions" not in result:
                    continue

                conflict = result["cr"]
                opinions = result["opinions"]

                if len(opinions) != 2:
                    continue

                # Get conflict analysis using CRDL
                analysis = self.conflict_manager.crdl_resolver.analyze_conflict(
                    opinion1=opinions[0],
                    opinion2=opinions[1],
                    opinion1_context=self.conflict_manager._get_opinion_context(
                        self.db, opinions[0]
                    ),
                    opinion2_context=self.conflict_manager._get_opinion_context(
                        self.db, opinions[1]
                    ),
                    additional_context=self.conflict_manager._get_additional_context(
                        self.db, conflict
                    ),
                )

                analyses.append(
                    {
                        "conflict_topic": conflict["topic"],
                        "status": conflict["status"],
                        "analysis": analysis.dict(),
                        "opinions": [
                            {
                                "statement": o["statement"],
                                "confidence": o["confidence"],
                                "stance": o["stance"],
                            }
                            for o in opinions
                        ],
                    }
                )

            return analyses

        except Exception as e:
            logger.error(f"Failed to get conflict analysis: {str(e)}")
            return []
