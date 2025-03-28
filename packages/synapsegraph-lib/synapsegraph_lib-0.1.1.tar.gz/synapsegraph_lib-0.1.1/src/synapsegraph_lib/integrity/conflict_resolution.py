"""
Conflict Resolution Module for SynapseGraph.

This module handles the detection, tracking, and resolution of contradictions
between opinions in the knowledge graph. It creates ConflictResolution nodes
to track contradictions and provides mechanisms for resolving them.
"""

import logging
from typing import List, Optional, Tuple, Dict, Any, Union
from datetime import datetime

from synapsegraph_lib.core.config import ConflictStatus
from synapsegraph_lib.core.database import Neo4jConnection
from synapsegraph_lib.core.models import Opinion, ConflictResolution
from synapsegraph_lib.synthesis.opinion_formation import OpinionSynthesizer
from synapsegraph_lib.integrity.conflict_resolution_llm import (
    ConflictResolutionLLM,
    ConflictAnalysis,
)

logger = logging.getLogger(__name__)


class ConflictManager:
    """
    Manages contradictions between opinions in the knowledge graph.

    This class is responsible for:
    1. Detecting contradictions between opinions
    2. Creating ConflictResolution nodes to track these contradictions
    3. Establishing relationships between contradicting opinions and resolution nodes
    4. Providing mechanisms for resolving contradictions using LLM-based analysis
    """

    def __init__(self, opinion_synthesizer: Optional[OpinionSynthesizer] = None):
        """
        Initialize the ConflictManager.

        Args:
            opinion_synthesizer: OpinionSynthesizer instance for detecting contradictions
        """
        if opinion_synthesizer:
            self.opinion_synthesizer = opinion_synthesizer
        else:
            # Create a TemporalManager to pass to OpinionSynthesizer
            from synapsegraph_lib.temporal.temporal_management import TemporalManager

            temporal_manager = TemporalManager()
            self.opinion_synthesizer = OpinionSynthesizer(
                temporal_manager=temporal_manager
            )

        self.crdl_resolver = ConflictResolutionLLM()

    def detect_and_track_contradictions(
        self, db: Neo4jConnection, threshold: float = 0.7, auto_resolve: bool = False
    ) -> List[ConflictResolution]:
        """
        Detect contradictions and create ConflictResolution nodes to track them.

        Args:
            db: Neo4j connection
            threshold: Confidence threshold for considering contradictions
            auto_resolve: Whether to attempt automatic resolution

        Returns:
            List of created ConflictResolution objects
        """
        # Find contradictions using the opinion synthesizer module
        contradictions = self.opinion_synthesizer.find_contradictions(db, threshold)

        if not contradictions:
            logger.info("No contradictions found")
            return []

        logger.info(f"Found {len(contradictions)} contradictions to track")

        # Create ConflictResolution nodes for each contradiction
        conflict_resolutions = []
        for opinion1, opinion2, priority_score in contradictions:
            # Check if a conflict resolution already exists for these opinions
            existing_resolution = self._find_existing_resolution(db, opinion1, opinion2)

            if existing_resolution:
                logger.info(f"Conflict already tracked: {existing_resolution.topic}")
                conflict_resolutions.append(existing_resolution)
                continue

            # Create a new conflict resolution
            conflict_resolution = self._create_conflict_resolution(
                db, opinion1, opinion2, priority_score
            )
            conflict_resolutions.append(conflict_resolution)

            # Attempt automatic resolution if requested
            if auto_resolve:
                self.resolve_conflict(db, conflict_resolution)

        return conflict_resolutions

    def _find_existing_resolution(
        self, db: Neo4jConnection, opinion1: Opinion, opinion2: Opinion
    ) -> Optional[ConflictResolution]:
        """
        Check if a conflict resolution already exists for the given opinions.

        Args:
            db: Neo4j connection
            opinion1: First opinion
            opinion2: Second opinion

        Returns:
            Existing ConflictResolution if found, None otherwise
        """
        query = """
        MATCH (o1:Opinion {uid: $uid1})-[:PART_OF_CONFLICT]->(cr:ConflictResolution)<-[:PART_OF_CONFLICT]-(o2:Opinion {uid: $uid2})
        RETURN cr
        """

        params = {"uid1": opinion1.uid, "uid2": opinion2.uid}

        try:
            result = db.execute_query(query, params, fetch_all=True)
            if result and result[0].get("cr"):
                cr_data = dict(result[0]["cr"])
                return ConflictResolution.from_dict(cr_data)
            return None
        except Exception as e:
            logger.error(f"Error finding existing conflict resolution: {str(e)}")
            return None

    def _create_conflict_resolution(
        self,
        db: Neo4jConnection,
        opinion1: Opinion,
        opinion2: Opinion,
        priority_score: float,
    ) -> ConflictResolution:
        """
        Create a ConflictResolution node and establish relationships.

        Args:
            db: Neo4j connection
            opinion1: First opinion
            opinion2: Second opinion
            priority_score: Priority score for the conflict

        Returns:
            Created ConflictResolution object
        """
        # Generate a topic based on the opinions
        topic = (
            f"Conflict: {opinion1.statement[:50]}... vs {opinion2.statement[:50]}..."
        )

        # Create the conflict resolution object
        conflict_resolution = ConflictResolution(
            topic=topic,
            status=ConflictStatus.ACTIVE,
            description=f"Contradiction between opinions with UIDs {opinion1.uid} and {opinion2.uid}",
            resolution_details="",
            priority=priority_score,
            metadata={
                "created_at": datetime.now().isoformat(),
                "opinion1_uid": opinion1.uid,
                "opinion2_uid": opinion2.uid,
                "opinion1_confidence": opinion1.confidence,
                "opinion2_confidence": opinion2.confidence,
            },
        )

        # Save the conflict resolution to the database
        conflict_resolution.save(db)

        # Create relationships between opinions and conflict resolution
        self._create_conflict_relationships(db, conflict_resolution, opinion1, opinion2)

        logger.info(f"Created conflict resolution: {conflict_resolution.topic}")
        return conflict_resolution

    def _create_conflict_relationships(
        self,
        db: Neo4jConnection,
        conflict_resolution: ConflictResolution,
        opinion1: Opinion,
        opinion2: Opinion,
    ) -> None:
        """
        Create relationships between opinions and conflict resolution.

        Args:
            db: Neo4j connection
            conflict_resolution: ConflictResolution object
            opinion1: First opinion
            opinion2: Second opinion
        """
        query = """
        MATCH (o1:Opinion {uid: $uid1})
        MATCH (o2:Opinion {uid: $uid2})
        MATCH (cr:ConflictResolution {topic: $topic})
        MERGE (o1)-[:PART_OF_CONFLICT]->(cr)
        MERGE (o2)-[:PART_OF_CONFLICT]->(cr)
        """

        params = {
            "uid1": opinion1.uid,
            "uid2": opinion2.uid,
            "topic": conflict_resolution.topic,
        }

        try:
            db.execute_query(query, params)
            logger.info(
                f"Created relationships for conflict resolution: {conflict_resolution.topic}"
            )
        except Exception as e:
            logger.error(f"Error creating conflict relationships: {str(e)}")

    def resolve_conflict(
        self,
        db: Neo4jConnection,
        conflict: ConflictResolution,
        resolution_status: ConflictStatus = ConflictStatus.RESOLVED,
        resolution_details: str = None,
        manual_resolution: bool = False,
    ) -> ConflictResolution:
        """
        Resolve a conflict using the CRDL approach or manual resolution.

        Args:
            db: Database connection
            conflict: The conflict to resolve
            resolution_status: The new status for the conflict
            resolution_details: Optional details about the resolution
            manual_resolution: Whether the resolution was done manually

        Returns:
            ConflictResolution: The updated conflict resolution
        """
        try:
            if manual_resolution:
                # Update conflict status and details
                conflict.status = resolution_status
                conflict.resolution_details = (
                    resolution_details or "No details provided"
                )
                conflict.metadata["resolution_details"] = (
                    resolution_details or "No details provided"
                )
                conflict.metadata["resolution_type"] = "manual"
                conflict.metadata["resolved_at"] = datetime.now().isoformat()

                # Save updated conflict to database
                query = """
                MATCH (c:ConflictResolution {uid: $uid})
                SET c.status = $status,
                    c.metadata = $metadata,
                    c.resolution_details = $resolution_details,
                    c.resolved_at = datetime()
                RETURN c
                """
                params = {
                    "uid": conflict.uid,
                    "status": resolution_status.value,
                    "metadata": conflict.metadata,
                    "resolution_details": resolution_details or "No details provided",
                }

                if db.execute_write_transaction(query, params):
                    return conflict
                else:
                    logger.error("Failed to update conflict resolution status")
                    return conflict

            else:
                # Get the conflicting opinions
                opinions = self._get_conflicting_opinions(db, conflict)
                if not opinions or len(opinions) != 2:
                    logger.error("Failed to retrieve conflicting opinions")
                    return conflict

                opinion1, opinion2 = opinions

                # Get additional context for the opinions
                opinion1_context = self._get_opinion_context(db, opinion1)
                opinion2_context = self._get_opinion_context(db, opinion2)
                additional_context = self._get_additional_context(db, conflict)

                # Analyze the conflict using CRDL
                analysis = self.crdl_resolver.analyze_conflict(
                    opinion1=opinion1,
                    opinion2=opinion2,
                    opinion1_context=opinion1_context,
                    opinion2_context=opinion2_context,
                    additional_context=additional_context,
                )

                # Resolve the conflict based on the analysis
                if self.crdl_resolver.resolve_conflict(db, conflict, analysis):
                    conflict.status = ConflictStatus.RESOLVED
                    conflict.resolution_details = analysis.reasoning
                    conflict.metadata["resolution_details"] = analysis.reasoning
                    conflict.metadata["resolution_type"] = "automatic"
                    conflict.metadata["resolved_at"] = datetime.now().isoformat()
                    conflict.metadata["analysis"] = analysis.to_dict()

                    # Save updated conflict to database
                    query = """
                    MATCH (c:ConflictResolution {uid: $uid})
                    SET c.status = $status,
                        c.metadata = $metadata,
                        c.resolution_details = $resolution_details,
                        c.resolved_at = datetime()
                    RETURN c
                    """
                    params = {
                        "uid": conflict.uid,
                        "status": conflict.status.value,
                        "metadata": conflict.metadata,
                        "resolution_details": analysis.reasoning,
                    }

                    if not db.execute_write_transaction(query, params):
                        logger.error("Failed to update conflict resolution status")
                        return conflict

                return conflict

        except Exception as e:
            logging.error(f"Error resolving conflict: {str(e)}")
            return conflict

    def _get_opinion_context(self, db: Neo4jConnection, opinion: Opinion) -> str:
        """
        Get additional context for an opinion.

        Args:
            db: Neo4j database connection
            opinion: Opinion to get context for

        Returns:
            Context string
        """
        query = """
        MATCH (o:Opinion {uid: $uid})
        MATCH (o)-[:BASED_ON]->(b:Belief)
        MATCH (b)<-[:BELIEVED_BY]-(s:Source)
        RETURN collect(DISTINCT b.statement) as beliefs,
               collect(DISTINCT s.name) as sources
        """
        result = db.execute_query_single(query, {"uid": opinion.uid})
        if not result:
            return ""

        beliefs = result.get("beliefs", [])
        sources = result.get("sources", [])
        return f"Based on beliefs: {', '.join(beliefs[:3])}...\nSources: {', '.join(sources)}"

    def _get_additional_context(
        self, db: Neo4jConnection, conflict_resolution: ConflictResolution
    ) -> str:
        """
        Get additional context about the conflict.

        Args:
            db: Neo4j database connection
            conflict_resolution: ConflictResolution object

        Returns:
            Additional context string
        """
        query = """
        MATCH (cr:ConflictResolution {topic: $topic})
        MATCH (cr)<-[:PART_OF_CONFLICT]-(o:Opinion)
        MATCH (o)-[:BASED_ON]->(b:Belief)
        RETURN count(DISTINCT o) as opinion_count,
               count(DISTINCT b) as belief_count,
               collect(DISTINCT b.category) as categories
        """
        result = db.execute_query_single(query, {"topic": conflict_resolution.topic})
        if not result:
            return ""

        return f"Conflict involves {result['opinion_count']} opinions and {result['belief_count']} beliefs across categories: {', '.join(result['categories'])}"

    def _get_conflicting_opinions(
        self, db: Neo4jConnection, conflict_resolution: ConflictResolution
    ) -> Optional[Tuple[Opinion, Opinion]]:
        """
        Get the conflicting opinions for a conflict resolution.

        Args:
            db: Neo4j database connection
            conflict_resolution: ConflictResolution object

        Returns:
            Tuple of conflicting opinions if found, None otherwise
        """
        query = """
        MATCH (cr:ConflictResolution {topic: $topic})
        MATCH (cr)<-[:PART_OF_CONFLICT]-(o:Opinion)
        RETURN o
        """
        results = db.execute_query(
            query, {"topic": conflict_resolution.topic}, fetch_all=True
        )

        if not results or len(results) != 2:
            return None

        opinions = []
        for result in results:
            if "o" in result:
                opinions.append(Opinion.from_dict(dict(result["o"])))

        return tuple(opinions) if len(opinions) == 2 else None

    def get_active_conflicts(self, db: Neo4jConnection) -> List[ConflictResolution]:
        """
        Get all active conflicts in the database.

        Args:
            db: Neo4j connection

        Returns:
            List of active ConflictResolution objects
        """
        query = """
        MATCH (cr:ConflictResolution {status: $status})
        RETURN cr
        """

        params = {"status": ConflictStatus.ACTIVE.value}

        try:
            results = db.execute_query(query, params, fetch_all=True)
            return [
                ConflictResolution.from_dict(dict(result["cr"])) for result in results
            ]
        except Exception as e:
            logger.error(f"Error getting active conflicts: {str(e)}")
            return []

    def get_conflict_opinions(
        self, db: Neo4jConnection, conflict_resolution: ConflictResolution
    ) -> List[Opinion]:
        """
        Get all opinions involved in a conflict.

        Args:
            db: Neo4j connection
            conflict_resolution: ConflictResolution object

        Returns:
            List of Opinion objects involved in the conflict
        """
        query = """
        MATCH (o:Opinion)-[:PART_OF_CONFLICT]->(cr:ConflictResolution {topic: $topic})
        RETURN o
        """

        params = {"topic": conflict_resolution.topic}

        try:
            results = db.execute_query(query, params, fetch_all=True)
            return [Opinion.from_dict(dict(result["o"])) for result in results]
        except Exception as e:
            logger.error(f"Error getting conflict opinions: {str(e)}")
            return []

    def detect_conflicts_for_topic(
        self, db: Neo4jConnection, topic: str
    ) -> List[Dict[str, Any]]:
        """
        Detect conflicts between opinions for a specific topic.

        Args:
            db: Neo4j database connection
            topic: The topic to analyze for conflicts

        Returns:
            List of conflict dictionaries
        """
        try:
            # Query to get all opinions for the topic
            query = """
            MATCH (o:Opinion)
            WHERE o.metadata CONTAINS $topic_json
            RETURN o
            """

            topic_json = f'{{"topic": "{topic}"}}'
            results = db.execute_query(
                query, {"topic_json": topic_json}, fetch_all=True
            )

            # Convert results to Opinion objects
            opinions = []
            for record in results:
                opinion_data = record.get("o", {})
                if opinion_data:
                    try:
                        # Create Opinion object
                        opinion = Opinion(
                            uid=opinion_data.get("uid", ""),
                            statement=opinion_data.get("statement", ""),
                            stance=opinion_data.get("stance", ""),
                            confidence=opinion_data.get("confidence", 0.0),
                            clarity=opinion_data.get("clarity", 0.0),
                            time_horizon=opinion_data.get("time_horizon", ""),
                            metadata=opinion_data.get("metadata", "{}"),
                        )
                        opinions.append(opinion)
                    except Exception as e:
                        logger.error(f"Error creating Opinion object: {str(e)}")

            if not opinions:
                logger.info(f"No opinions found for topic '{topic}'")
                return []

            # Find contradictions between opinions
            contradictions = []
            for i in range(len(opinions)):
                for j in range(i + 1, len(opinions)):
                    # Check for opposing stances
                    if (
                        opinions[i].stance == "Supportive"
                        and opinions[j].stance == "Opposed"
                    ) or (
                        opinions[i].stance == "Opposed"
                        and opinions[j].stance == "Supportive"
                    ):
                        # Create a conflict dictionary
                        conflict = {
                            "uid": f"conflict_{opinions[i].uid}_{opinions[j].uid}",
                            "opinion1": opinions[i].uid,
                            "opinion2": opinions[j].uid,
                            "opinion1_statement": opinions[i].statement,
                            "opinion2_statement": opinions[j].statement,
                            "opinion1_stance": opinions[i].stance,
                            "opinion2_stance": opinions[j].stance,
                            "topic": topic,
                            "detected_at": datetime.now().isoformat(),
                            "status": "active",
                        }
                        contradictions.append(conflict)

            logger.info(f"Found {len(contradictions)} conflicts for topic '{topic}'")
            return contradictions

        except Exception as e:
            logger.error(f"Error detecting conflicts for topic '{topic}': {str(e)}")
            return []

    def get_active_conflicts(self, db: Neo4jConnection) -> List[Dict[str, Any]]:
        """
        Get all active conflicts from the database.

        Args:
            db: Neo4j database connection

        Returns:
            List of active conflict dictionaries
        """
        try:
            # Query to get all active conflicts
            query = """
            MATCH (c:ConflictResolution)
            WHERE c.status = 'ACTIVE'
            RETURN c
            """

            results = db.execute_query(query, fetch_all=True)

            # Convert results to conflict dictionaries
            conflicts = []
            for record in results:
                conflict_data = record.get("c", {})
                if conflict_data:
                    conflicts.append(
                        {
                            "uid": conflict_data.get("uid", ""),
                            "status": conflict_data.get("status", ""),
                            "created_at": conflict_data.get("created_at", ""),
                            "updated_at": conflict_data.get("updated_at", ""),
                            "resolution_strategy": conflict_data.get(
                                "resolution_strategy", ""
                            ),
                            "resolution_notes": conflict_data.get(
                                "resolution_notes", ""
                            ),
                        }
                    )

            logger.info(f"Found {len(conflicts)} active conflicts")
            return conflicts

        except Exception as e:
            logger.error(f"Error getting active conflicts: {str(e)}")
            return []

    def get_resolved_conflicts(self, db: Neo4jConnection) -> List[Dict[str, Any]]:
        """
        Get all resolved conflicts from the database.

        Args:
            db: Neo4j database connection

        Returns:
            List of resolved conflict dictionaries
        """
        try:
            # Query to get all resolved conflicts
            query = """
            MATCH (c:ConflictResolution)
            WHERE c.status = 'RESOLVED'
            RETURN c
            """

            results = db.execute_query(query, fetch_all=True)

            # Convert results to conflict dictionaries
            conflicts = []
            for record in results:
                conflict_data = record.get("c", {})
                if conflict_data:
                    conflicts.append(
                        {
                            "uid": conflict_data.get("uid", ""),
                            "status": conflict_data.get("status", ""),
                            "created_at": conflict_data.get("created_at", ""),
                            "updated_at": conflict_data.get("updated_at", ""),
                            "resolution_strategy": conflict_data.get(
                                "resolution_strategy", ""
                            ),
                            "resolution_notes": conflict_data.get(
                                "resolution_notes", ""
                            ),
                        }
                    )

            logger.info(f"Found {len(conflicts)} resolved conflicts")
            return conflicts

        except Exception as e:
            logger.error(f"Error getting resolved conflicts: {str(e)}")
            return []

    def get_conflicts_for_topic(
        self, db: Neo4jConnection, topic: str
    ) -> List[ConflictResolution]:
        """
        Get all conflicts for a specific topic.

        Args:
            db: Neo4j connection
            topic: Topic to find conflicts for

        Returns:
            List of ConflictResolution objects for the topic
        """
        query = """
        MATCH (cr:ConflictResolution)
        WHERE toLower(cr.topic) CONTAINS toLower($topic)
        RETURN cr
        """

        try:
            results = db.execute_query(query, {"topic": topic}, fetch_all=True)
            return [ConflictResolution.from_dict(result["cr"]) for result in results]
        except Exception as e:
            logger.error(f"Failed to get conflicts for topic {topic}: {str(e)}")
            return []
