"""
Belief Manager module for SynapseGraph.

This module provides functionality for managing beliefs in the knowledge graph,
including updating beliefs using Bayesian-style probabilistic reasoning.
"""

import logging
from typing import Dict, List, Optional, Any, Union, Tuple
import datetime

from synapsegraph_lib.core.config import config
from synapsegraph_lib.core.models import Belief, Source, SpeculationMarker
from synapsegraph_lib.core.database import Neo4jConnection
from synapsegraph_lib.audit.audit_logger import AuditLogger

logger = logging.getLogger(__name__)


class BeliefManager:
    """
    Manages beliefs in the knowledge graph.

    This class is responsible for:
    1. Updating beliefs using Bayesian-style probabilistic reasoning
    2. Handling speculative beliefs
    3. Cross-validating beliefs with multiple sources
    4. Filtering noise from low-quality sources
    """

    def __init__(self, db: Neo4jConnection):
        """
        Initialize the BeliefManager.

        Args:
            db: Neo4j database connection
        """
        self.db = db
        self.audit_logger = AuditLogger(db)
        self.min_confidence_threshold = config.min_confidence_threshold
        self.contradiction_threshold = config.contradiction_threshold

    def update_belief(
        self,
        existing_belief: Belief,
        new_evidence_confidence: float,
        source: Source,
        reason: str = "New evidence",
    ) -> Optional[Belief]:
        """
        Update an existing belief with new evidence using Bayesian-style reasoning.

        Args:
            existing_belief: The existing belief to update
            new_evidence_confidence: Confidence score of the new evidence (0.0 to 1.0)
            source: Source of the new evidence
            reason: Reason for the update

        Returns:
            Updated belief if successful, None otherwise
        """
        # 1. Noise Filtering - Skip updates from low-quality or irrelevant sources
        if self._should_filter_source(source):
            logger.info(f"Filtering update from low-quality source: {source.name}")
            return existing_belief

        # 2. Cross-Validation for high-impact evidence
        if self._is_high_impact_update(existing_belief, new_evidence_confidence):
            if not self._is_cross_validated(existing_belief, source):
                # Mark as speculative until cross-validated
                existing_belief.speculative = True
                logger.info(
                    f"Marking high-impact belief as speculative until cross-validated: {existing_belief.statement}"
                )

        # 3. Calculate new confidence using Bayesian-style update
        prior = existing_belief.confidence
        source_trust = source.trust_score

        # Bayesian-style update formula from directive
        new_confidence = min(
            0.99,
            max(0.01, prior + (new_evidence_confidence * source_trust * (1 - prior))),
        )

        # 4. Handle speculative beliefs
        if existing_belief.speculative:
            # Cap confidence of speculative beliefs at 0.6
            new_confidence = min(new_confidence, 0.6)

            # Only increase confidence of speculative beliefs if source is highly trusted
            if source.trust_score >= 0.8 and new_evidence_confidence > prior:
                # Allow confidence to increase but still cap at 0.6
                pass
            elif new_evidence_confidence < prior:
                # Allow confidence to decrease
                pass
            else:
                # Otherwise, maintain current confidence
                new_confidence = prior

        # Create a copy of the existing belief with updated confidence
        updated_belief = Belief(
            statement=existing_belief.statement,
            confidence=new_confidence,
            last_updated=datetime.datetime.now(),
            expires_at=existing_belief.expires_at,
            version=existing_belief.version + 1,
            category=existing_belief.category,
            speculative=existing_belief.speculative,
            metadata=existing_belief.metadata.copy(),
        )

        # Save the updated belief
        if updated_belief.save(self.db):
            # Log the belief update
            self.audit_logger.log_belief_update(
                node_id=updated_belief.uid,
                previous_confidence=existing_belief.confidence,
                new_confidence=updated_belief.confidence,
                previous_version=existing_belief.version,
                new_version=updated_belief.version,
                updated_by=source.name,
                reason=reason,
            )

            # If the belief was linked to entities or sources, recreate those links
            self._recreate_belief_links(existing_belief, updated_belief)

            logger.info(
                f"Updated belief: {updated_belief.statement} (confidence: {existing_belief.confidence:.2f} -> {updated_belief.confidence:.2f})"
            )
            return updated_belief
        else:
            logger.error(f"Failed to save updated belief: {updated_belief.statement}")
            return None

    def find_or_update_belief(
        self,
        statement: str,
        confidence: float,
        source: Source,
        category: str = "",
        speculative: bool = False,
    ) -> Optional[Belief]:
        """
        Find an existing belief or create a new one.

        Args:
            statement: The belief statement
            confidence: Confidence score of the belief (0.0 to 1.0)
            source: Source of the belief
            category: Category of the belief
            speculative: Whether the belief is speculative

        Returns:
            Belief instance if successful, None otherwise
        """
        # Try to find an existing belief with the same statement
        existing_belief = self._find_belief_by_statement(statement)

        if existing_belief:
            # Update the existing belief
            return self.update_belief(existing_belief, confidence, source)
        else:
            # Create a new belief
            new_belief = Belief(
                statement=statement,
                confidence=min(
                    0.99, max(0.01, confidence * source.trust_score)
                ),  # Adjust initial confidence by source trust
                last_updated=datetime.datetime.now(),
                version=1,
                category=category,
                speculative=speculative,
                metadata={},
            )

            # Save the new belief
            if new_belief.save(self.db):
                # Link to source
                if not new_belief.link_to_source(self.db, source):
                    logger.error(
                        f"Failed to link new belief to source: {new_belief.statement} -> {source.name}"
                    )

                logger.info(
                    f"Created new belief: {new_belief.statement} (confidence: {new_belief.confidence:.2f})"
                )
                return new_belief
            else:
                logger.error(f"Failed to save new belief: {new_belief.statement}")
                return None

    def mark_belief_as_speculative(
        self, belief: Belief, reason: str = "Insufficient evidence"
    ) -> bool:
        """
        Mark a belief as speculative.

        Args:
            belief: The belief to mark as speculative
            reason: Reason for marking as speculative

        Returns:
            True if successful, False otherwise
        """
        # Create a speculation marker
        marker = SpeculationMarker(
            reason=reason,
            validation_criteria="Requires confirmation from at least two trusted sources",
        )

        # Save the marker
        if marker.save(self.db):
            # Mark the belief as speculative
            belief.speculative = True

            # Save the updated belief
            if belief.save(self.db):
                # Link the belief to the marker
                if belief.mark_as_speculative(self.db, marker):
                    logger.info(f"Marked belief as speculative: {belief.statement}")
                    return True
                else:
                    logger.error(
                        f"Failed to link belief to speculation marker: {belief.statement}"
                    )
                    return False
            else:
                logger.error(f"Failed to save updated belief: {belief.statement}")
                return False
        else:
            logger.error("Failed to save speculation marker")
            return False

    def _find_belief_by_statement(self, statement: str) -> Optional[Belief]:
        """
        Find a belief by its statement.

        Args:
            statement: The belief statement

        Returns:
            Belief instance if found, None otherwise
        """
        query = """
        MATCH (b:Belief {statement: $statement})
        RETURN b
        """

        try:
            result = self.db.execute_query_single(query, {"statement": statement})
            if result and "b" in result:
                return Belief.from_dict(dict(result["b"]))
            return None
        except Exception as e:
            logger.error(f"Failed to find belief by statement: {statement}: {str(e)}")
            return None

    def _should_filter_source(self, source: Source) -> bool:
        """
        Determine if a source should be filtered out due to low quality.

        Args:
            source: The source to check

        Returns:
            True if the source should be filtered, False otherwise
        """
        # Filter out sources with very low trust scores
        if source.trust_score < config.min_source_trust:
            return True

        # Filter out unverified sources for critical updates
        if source.verification_status != "Verified" and source.trust_score < 0.7:
            return True

        return False

    def _is_high_impact_update(self, belief: Belief, new_confidence: float) -> bool:
        """
        Determine if an update would have a high impact on the belief.

        Args:
            belief: The existing belief
            new_confidence: The new confidence score

        Returns:
            True if the update would have a high impact, False otherwise
        """
        # Calculate the absolute difference in confidence
        confidence_diff = abs(belief.confidence - new_confidence)

        # Consider it high impact if the difference is significant
        return confidence_diff > 0.3

    def _is_cross_validated(self, belief: Belief, source: Source) -> bool:
        """Check if a belief has been cross-validated by independent sources.

        Args:
            belief: The belief to check
            source: The current source

        Returns:
            bool: True if the belief has been cross-validated by independent sources
        """
        try:
            # Query to count sources that support this belief
            query = """
            MATCH (b:Belief {uid: $belief_uid})<-[:SUPPORTS]-(s:Source)
            WHERE s.type <> $source_type
            RETURN count(DISTINCT s) as source_count
            """

            result = self.db.execute_query(
                query, {"belief_uid": belief.uid, "source_type": source.type}
            )

            # Handle both list and dictionary response formats
            if isinstance(result, dict):
                source_count = result.get("source_count", 0)
            elif isinstance(result, list) and len(result) > 0:
                source_count = result[0].get("source_count", 0)
            else:
                source_count = 0

            return source_count > 0

        except Exception as e:
            logger.error(f"Error checking cross-validation: {str(e)}")
            return False

    def _recreate_belief_links(self, old_belief: Belief, new_belief: Belief) -> bool:
        """
        Recreate links from the old belief to the new belief.

        Args:
            old_belief: The old belief
            new_belief: The new belief

        Returns:
            True if successful, False otherwise
        """
        # Copy entity links
        query_entities = """
        MATCH (e:Entity)-[:BELIEVES]->(b:Belief {statement: $statement})
        RETURN e
        """

        try:
            results = self.db.execute_query(
                query_entities, {"statement": old_belief.statement}
            )
            for result in results:
                if "e" in result:
                    entity = result["e"]
                    entity_query = """
                    MATCH (e:Entity {name: $entity_name})
                    MATCH (b:Belief {statement: $statement})
                    MERGE (e)-[r:BELIEVES]->(b)
                    ON CREATE SET r.created_at = datetime($created_at)
                    RETURN r
                    """

                    entity_params = {
                        "entity_name": entity["name"],
                        "statement": new_belief.statement,
                        "created_at": datetime.datetime.now().isoformat(),
                    }

                    self.db.execute_write_transaction(entity_query, entity_params)
        except Exception as e:
            logger.error(
                f"Failed to recreate entity links for belief: {new_belief.statement}: {str(e)}"
            )
            return False

        # Copy source links
        query_sources = """
        MATCH (b:Belief {statement: $statement})-[r:SUPPORTED_BY|CONTRADICTED_BY]->(s:Source)
        RETURN s, type(r) as relationship_type
        """

        try:
            results = self.db.execute_query(
                query_sources, {"statement": old_belief.statement}
            )
            for result in results:
                if "s" in result and "relationship_type" in result:
                    source = result["s"]
                    relationship_type = result["relationship_type"]

                    source_query = f"""
                    MATCH (b:Belief {{statement: $statement}})
                    MATCH (s:Source {{name: $source_name}})
                    MERGE (b)-[r:{relationship_type}]->(s)
                    ON CREATE SET r.created_at = datetime($created_at)
                    RETURN r
                    """

                    source_params = {
                        "statement": new_belief.statement,
                        "source_name": source["name"],
                        "created_at": datetime.datetime.now().isoformat(),
                    }

                    self.db.execute_write_transaction(source_query, source_params)
        except Exception as e:
            logger.error(
                f"Failed to recreate source links for belief: {new_belief.statement}: {str(e)}"
            )
            return False

        return True

    def update_belief_with_conditional_dependencies(
        self,
        belief: Belief,
        new_evidence_confidence: float,
        source: Source,
        related_beliefs: List[Tuple[Belief, float]],
        reason: str = "New evidence with conditional dependencies",
    ) -> Dict[str, Any]:
        """
        Update a belief and propagate updates to related beliefs based on conditional probabilities.

        Args:
            belief: The primary belief to update
            new_evidence_confidence: Confidence score of the new evidence (0.0 to 1.0)
            source: Source of the new evidence
            related_beliefs: List of tuples containing (related_belief, conditional_probability)
            reason: Reason for the update

        Returns:
            Dictionary with updated beliefs and their update status
        """
        # Update the primary belief
        updated_primary = self.update_belief(
            belief, new_evidence_confidence, source, reason=reason
        )

        results = {
            "primary_belief": {
                "statement": belief.statement,
                "previous_confidence": belief.confidence,
                "new_confidence": (
                    updated_primary.confidence if updated_primary else belief.confidence
                ),
                "success": updated_primary is not None,
            },
            "related_beliefs": [],
        }

        # If primary update failed, return early
        if not updated_primary:
            return results

        # Calculate confidence change in primary belief
        confidence_delta = updated_primary.confidence - belief.confidence

        # Update related beliefs based on conditional probabilities
        for related_belief, conditional_prob in related_beliefs:
            # Calculate impact on related belief based on conditional probability
            impact_factor = conditional_prob * confidence_delta

            # Skip if impact is negligible
            if abs(impact_factor) < 0.01:
                results["related_beliefs"].append(
                    {
                        "statement": related_belief.statement,
                        "previous_confidence": related_belief.confidence,
                        "new_confidence": related_belief.confidence,
                        "success": True,
                        "skipped": True,
                        "reason": "Negligible impact",
                    }
                )
                continue

            # Calculate new confidence for related belief
            new_related_confidence = min(
                0.99, max(0.01, related_belief.confidence + impact_factor)
            )

            # Create a synthetic source that represents the conditional update
            conditional_source = Source(
                name=f"Conditional update from {belief.statement}",
                trust_score=source.trust_score
                * conditional_prob,  # Reduce trust proportionally
                type=source.type,
                metadata={
                    "parent_belief": belief.statement,
                    "parent_belief_uid": belief.uid,
                    "conditional_probability": conditional_prob,
                    "original_source": source.name,
                },
            )

            # Update the related belief
            related_update_reason = (
                f"Conditional update from related belief: {belief.statement}"
            )
            updated_related = self.update_belief(
                related_belief,
                new_related_confidence,
                conditional_source,
                reason=related_update_reason,
            )

            results["related_beliefs"].append(
                {
                    "statement": related_belief.statement,
                    "previous_confidence": related_belief.confidence,
                    "new_confidence": (
                        updated_related.confidence
                        if updated_related
                        else related_belief.confidence
                    ),
                    "success": updated_related is not None,
                    "conditional_probability": conditional_prob,
                    "impact_factor": impact_factor,
                }
            )

        return results

    def find_related_beliefs(
        self, db: Neo4jConnection, belief: Belief, min_similarity: float = 0.3
    ) -> List[Tuple[Belief, float]]:
        """Find beliefs related to the given belief based on shared entities, direct relationships, or content similarity.

        Args:
            db: Neo4j database connection
            belief: The belief to find related beliefs for
            min_similarity: Minimum similarity score to include a belief (default: 0.3)

        Returns:
            List of tuples containing (related_belief, similarity_score), sorted by similarity
        """
        related_beliefs = []

        try:
            # Query 1: Find beliefs with shared entities
            shared_entities_query = """
            MATCH (b1:Belief {uid: $belief_uid})-[:BELIEVES_IN]->(e:Entity)<-[:BELIEVES_IN]-(b2:Belief)
            WHERE b1.uid <> b2.uid
            WITH b2 as b, count(e) as shared_entities
            WHERE shared_entities >= $min_entities
            RETURN b, shared_entities
            """

            # Query 2: Find beliefs with direct relationships
            direct_relations_query = """
            MATCH (b1:Belief {uid: $belief_uid})-[r:RELATES_TO]-(b2:Belief)
            WHERE r.strength >= $min_similarity
            RETURN b2 as b, r.strength as relation_strength
            """

            # Query 3: Find beliefs with similar content
            content_similarity_query = """
            MATCH (b1:Belief {uid: $belief_uid}), (b2:Belief)
            WHERE b1.uid <> b2.uid
            WITH b1, b2, 
                 gds.similarity.cosine(b1.embedding, b2.embedding) as similarity
            WHERE similarity >= $min_similarity
            RETURN b2 as b, similarity
            """

            # Execute queries and collect results
            belief_map = {}  # Use a map to deduplicate beliefs

            # Query 1 results - shared entities
            shared_entities_results = db.execute_query(
                shared_entities_query,
                {
                    "belief_uid": belief.uid,
                    "min_entities": max(
                        1, int(5 * min_similarity)
                    ),  # Scale min entities with similarity threshold
                },
            )
            for result in shared_entities_results:
                if "b" in result:
                    b2_data = result["b"]
                    shared_entities = result.get("shared_entities", 0)
                    similarity = min(1.0, shared_entities / 5.0)  # Normalize to 0-1
                    if similarity >= min_similarity:
                        belief_map[b2_data.get("uid")] = (b2_data, similarity)

            # Query 2 results - direct relations
            direct_relations_results = db.execute_query(
                direct_relations_query,
                {"belief_uid": belief.uid, "min_similarity": min_similarity},
            )
            for result in direct_relations_results:
                if "b" in result:
                    b2_data = result["b"]
                    relation_strength = result.get("relation_strength", 0.0)
                    if relation_strength >= min_similarity:
                        belief_map[b2_data.get("uid")] = (b2_data, relation_strength)

            # Query 3 results - content similarity
            content_similarity_results = db.execute_query(
                content_similarity_query,
                {"belief_uid": belief.uid, "min_similarity": min_similarity},
            )
            for result in content_similarity_results:
                if "b" in result:
                    b2_data = result["b"]
                    similarity = result.get("similarity", 0.0)
                    if similarity >= min_similarity:
                        belief_map[b2_data.get("uid")] = (b2_data, similarity)

            # Convert results to Belief objects
            for b2_data, similarity in belief_map.values():
                related_belief = Belief(
                    uid=b2_data.get("uid", ""),
                    statement=b2_data.get("statement", ""),
                    confidence=b2_data.get("confidence", 0.0),
                    version=b2_data.get("version", 1),
                    speculative=b2_data.get("speculative", False),
                )
                related_beliefs.append((related_belief, similarity))

            # Sort by similarity score in descending order
            related_beliefs.sort(key=lambda x: x[1], reverse=True)

        except Exception as e:
            logger.error(f"Error finding related beliefs: {str(e)}")

        return related_beliefs
