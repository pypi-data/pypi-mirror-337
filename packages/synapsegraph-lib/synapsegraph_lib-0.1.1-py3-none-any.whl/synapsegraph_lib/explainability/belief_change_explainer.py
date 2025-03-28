import logging
from typing import List, Dict, Any, Optional, Tuple
import datetime
from enum import Enum

from synapsegraph_lib.core.models import Belief
from synapsegraph_lib.core.database import Neo4jConnection

logger = logging.getLogger(__name__)


class ChangeType(Enum):
    """Types of belief changes that can be explained."""

    CONFIDENCE_INCREASE = "confidence_increase"
    CONFIDENCE_DECREASE = "confidence_decrease"
    STATEMENT_REFINEMENT = "statement_refinement"
    CONTRADICTION = "contradiction"
    NEW_EVIDENCE = "new_evidence"
    TEMPORAL_DECAY = "temporal_decay"
    DOMAIN_SHIFT = "domain_shift"
    PARADIGM_SHIFT = "paradigm_shift"


class BeliefChangeExplainer:
    """
    Provides explanations for belief changes, offering transparency about
    why beliefs are updated and how they evolve over time.
    """

    def __init__(self):
        """Initialize the BeliefChangeExplainer."""
        logger.info("Initialized BeliefChangeExplainer")

    def explain_belief_change(
        self, db: Neo4jConnection, belief_uid: str
    ) -> Dict[str, Any]:
        """
        Generate an explanation for how a belief has changed over time.

        Args:
            db: Neo4j connection
            belief_uid: UID of the belief to explain

        Returns:
            Dictionary containing the explanation and change history
        """
        try:
            # Get the current belief
            current_belief = self._get_belief(db, belief_uid)
            if not current_belief:
                return {"error": f"Belief with UID {belief_uid} not found"}

            # Get the belief's version history
            history = self._get_belief_history(db, belief_uid)

            # Get sources that influenced this belief
            sources = self._get_belief_sources(db, belief_uid)

            # Analyze changes
            changes = self._analyze_changes(history)

            # Generate natural language explanation
            explanation = self._generate_explanation(
                current_belief, history, changes, sources
            )

            return {
                "belief": current_belief,
                "history": history,
                "changes": changes,
                "sources": sources,
                "explanation": explanation,
            }
        except Exception as e:
            logger.error(f"Error explaining belief change: {str(e)}")
            return {"error": str(e)}

    def _get_belief(
        self, db: Neo4jConnection, belief_uid: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get a belief by its UID.

        Args:
            db: Neo4j connection
            belief_uid: UID of the belief to get

        Returns:
            Belief data as a dictionary, or None if not found
        """
        query = """
        MATCH (b:Belief {uid: $uid})
        RETURN b
        """

        params = {"uid": belief_uid}

        result = db.execute_query(query, params)

        if result and "b" in result[0]:
            return dict(result[0]["b"])

        return None

    def _get_belief_history(
        self, db: Neo4jConnection, belief_uid: str
    ) -> List[Dict[str, Any]]:
        """
        Get the version history of a belief.

        Args:
            db: Neo4j connection
            belief_uid: UID of the belief

        Returns:
            List of historical versions of the belief
        """
        query = """
        MATCH (b:Belief {uid: $uid})-[:HAS_VERSION]->(v:BeliefVersion)
        RETURN v
        ORDER BY v.version ASC
        """

        params = {"uid": belief_uid}

        results = db.execute_query(query, params, fetch_all=True)

        history = []
        for result in results:
            if "v" in result:
                history.append(dict(result["v"]))

        return history

    def _get_belief_sources(
        self, db: Neo4jConnection, belief_uid: str
    ) -> List[Dict[str, Any]]:
        """
        Get the sources that influenced a belief.

        Args:
            db: Neo4j connection
            belief_uid: UID of the belief

        Returns:
            List of sources with their influence details
        """
        query = """
        MATCH (b:Belief {uid: $uid})-[r:DERIVED_FROM]->(s:Source)
        RETURN s, r.confidence_contribution as confidence_contribution, 
               r.timestamp as timestamp
        ORDER BY r.timestamp DESC
        """

        params = {"uid": belief_uid}

        results = db.execute_query(query, params, fetch_all=True)

        sources = []
        for result in results:
            if "s" in result:
                source_data = dict(result["s"])
                source_data["confidence_contribution"] = result.get(
                    "confidence_contribution", 0
                )
                source_data["timestamp"] = result.get("timestamp")
                sources.append(source_data)

        return sources

    def _analyze_changes(self, history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze the changes between belief versions.

        Args:
            history: List of historical versions of the belief

        Returns:
            List of changes with their details
        """
        changes = []

        if not history or len(history) < 2:
            return changes

        for i in range(1, len(history)):
            previous = history[i - 1]
            current = history[i]

            change = {
                "from_version": previous.get("version"),
                "to_version": current.get("version"),
                "timestamp": current.get("timestamp"),
                "changes": [],
            }

            # Check for confidence change
            prev_confidence = previous.get("confidence", 0)
            curr_confidence = current.get("confidence", 0)
            confidence_delta = curr_confidence - prev_confidence

            if abs(confidence_delta) > 0.01:  # Threshold for significant change
                change_type = (
                    ChangeType.CONFIDENCE_INCREASE
                    if confidence_delta > 0
                    else ChangeType.CONFIDENCE_DECREASE
                )
                change["changes"].append(
                    {
                        "type": change_type.value,
                        "previous_value": prev_confidence,
                        "current_value": curr_confidence,
                        "delta": confidence_delta,
                        "reason": current.get("update_reason", "No reason provided"),
                    }
                )

            # Check for statement refinement
            prev_statement = previous.get("statement", "")
            curr_statement = current.get("statement", "")

            if prev_statement != curr_statement:
                change["changes"].append(
                    {
                        "type": ChangeType.STATEMENT_REFINEMENT.value,
                        "previous_value": prev_statement,
                        "current_value": curr_statement,
                        "reason": current.get("update_reason", "No reason provided"),
                    }
                )

            # Add other change types based on metadata
            if "new_evidence" in current.get("metadata", {}):
                change["changes"].append(
                    {
                        "type": ChangeType.NEW_EVIDENCE.value,
                        "evidence": current.get("metadata", {}).get("new_evidence"),
                        "reason": current.get("update_reason", "No reason provided"),
                    }
                )

            if "temporal_decay" in current.get("metadata", {}):
                change["changes"].append(
                    {
                        "type": ChangeType.TEMPORAL_DECAY.value,
                        "decay_amount": current.get("metadata", {}).get(
                            "temporal_decay"
                        ),
                        "reason": "Time-based confidence decay",
                    }
                )

            if "domain_shift" in current.get("metadata", {}):
                change["changes"].append(
                    {
                        "type": ChangeType.DOMAIN_SHIFT.value,
                        "details": current.get("metadata", {}).get("domain_shift"),
                        "reason": current.get("update_reason", "No reason provided"),
                    }
                )

            if "paradigm_shift" in current.get("metadata", {}):
                change["changes"].append(
                    {
                        "type": ChangeType.PARADIGM_SHIFT.value,
                        "details": current.get("metadata", {}).get("paradigm_shift"),
                        "reason": current.get("update_reason", "No reason provided"),
                    }
                )

            if change["changes"]:
                changes.append(change)

        return changes

    def _generate_explanation(
        self,
        belief: Dict[str, Any],
        history: List[Dict[str, Any]],
        changes: List[Dict[str, Any]],
        sources: List[Dict[str, Any]],
    ) -> str:
        """
        Generate a natural language explanation of belief changes.

        Args:
            belief: Current belief data
            history: List of historical versions of the belief
            changes: List of analyzed changes
            sources: List of sources that influenced the belief

        Returns:
            Natural language explanation
        """
        if not history or len(history) < 2:
            return f"This belief '{belief.get('statement')}' has not changed since its creation."

        # Start with a summary
        explanation = [
            f"Belief: '{belief.get('statement')}' (confidence: {belief.get('confidence', 0):.2f})",
            f"This belief has changed {len(changes)} times since its creation on {history[0].get('timestamp')}.",
            "",
        ]

        # Add key changes
        explanation.append("Key changes:")

        for change in changes:
            timestamp = change.get("timestamp", "unknown time")
            explanation.append(
                f"• Version {change.get('from_version')} → {change.get('to_version')} ({timestamp}):"
            )

            for detail in change.get("changes", []):
                change_type = detail.get("type")

                if change_type == ChangeType.CONFIDENCE_INCREASE.value:
                    explanation.append(
                        f"  - Confidence increased from {detail.get('previous_value', 0):.2f} to "
                        f"{detail.get('current_value', 0):.2f} ({detail.get('delta', 0)*100:.1f}%)"
                    )
                    explanation.append(
                        f"    Reason: {detail.get('reason', 'No reason provided')}"
                    )

                elif change_type == ChangeType.CONFIDENCE_DECREASE.value:
                    explanation.append(
                        f"  - Confidence decreased from {detail.get('previous_value', 0):.2f} to "
                        f"{detail.get('current_value', 0):.2f} ({abs(detail.get('delta', 0))*100:.1f}%)"
                    )
                    explanation.append(
                        f"    Reason: {detail.get('reason', 'No reason provided')}"
                    )

                elif change_type == ChangeType.STATEMENT_REFINEMENT.value:
                    explanation.append(
                        f"  - Statement refined from '{detail.get('previous_value', '')}' to '{detail.get('current_value', '')}'"
                    )
                    explanation.append(
                        f"    Reason: {detail.get('reason', 'No reason provided')}"
                    )

                elif change_type == ChangeType.NEW_EVIDENCE.value:
                    explanation.append(
                        f"  - New evidence incorporated: {detail.get('evidence', 'Unknown evidence')}"
                    )

                elif change_type == ChangeType.TEMPORAL_DECAY.value:
                    explanation.append(
                        f"  - Confidence decayed due to time passage: {detail.get('decay_amount', 0):.2f}"
                    )

                elif change_type == ChangeType.DOMAIN_SHIFT.value:
                    explanation.append(
                        f"  - Domain knowledge shifted: {detail.get('details', 'No details provided')}"
                    )

                elif change_type == ChangeType.PARADIGM_SHIFT.value:
                    explanation.append(
                        f"  - Paradigm shift detected: {detail.get('details', 'No details provided')}"
                    )

            explanation.append("")

        # Add source influence
        if sources:
            explanation.append("Sources that influenced this belief:")
            for source in sources[:5]:  # Limit to top 5 sources
                contribution = source.get("confidence_contribution", 0)
                explanation.append(
                    f"• {source.get('name', 'Unknown source')}: "
                    f"contributed {contribution:.2f} to confidence"
                )

            if len(sources) > 5:
                explanation.append(f"... and {len(sources) - 5} more sources")

        return "\n".join(explanation)

    def create_belief_change_record(
        self,
        db: Neo4jConnection,
        belief: Belief,
        previous_belief: Optional[Dict[str, Any]],
        change_type: ChangeType,
        reason: str,
        details: Dict[str, Any] = None,
    ) -> bool:
        """
        Create a record of a belief change for explainability.

        Args:
            db: Neo4j connection
            belief: Current belief object
            previous_belief: Previous belief data (if available)
            change_type: Type of change
            reason: Reason for the change
            details: Additional details about the change

        Returns:
            True if successful, False otherwise
        """
        try:
            # Create a BeliefChange node
            query = """
            CREATE (c:BeliefChange {
                uid: randomUUID(),
                belief_uid: $belief_uid,
                change_type: $change_type,
                reason: $reason,
                details: $details,
                previous_confidence: $previous_confidence,
                current_confidence: $current_confidence,
                previous_statement: $previous_statement,
                current_statement: $current_statement,
                timestamp: datetime()
            })
            RETURN c.uid as uid
            """

            params = {
                "belief_uid": belief.uid,
                "change_type": change_type.value,
                "reason": reason,
                "details": details or {},
                "previous_confidence": (
                    previous_belief.get("confidence", 0) if previous_belief else 0
                ),
                "current_confidence": belief.confidence,
                "previous_statement": (
                    previous_belief.get("statement", "") if previous_belief else ""
                ),
                "current_statement": belief.statement,
            }

            result = db.execute_query(query, params)
            change_uid = result[0]["uid"] if result else None

            if not change_uid:
                logger.error("Failed to create belief change record")
                return False

            # Link the change record to the belief
            link_query = """
            MATCH (b:Belief {uid: $belief_uid})
            MATCH (c:BeliefChange {uid: $change_uid})
            CREATE (b)-[:HAS_CHANGE]->(c)
            """

            link_params = {"belief_uid": belief.uid, "change_uid": change_uid}

            db.execute_query(link_query, link_params)

            logger.info(
                f"Created belief change record for belief {belief.uid}: {change_type.value}"
            )
            return True
        except Exception as e:
            logger.error(f"Error creating belief change record: {str(e)}")
            return False

    def get_belief_change_timeline(
        self, db: Neo4jConnection, belief_uid: str
    ) -> List[Dict[str, Any]]:
        """
        Get a timeline of changes for a belief.

        Args:
            db: Neo4j connection
            belief_uid: UID of the belief

        Returns:
            List of change records in chronological order
        """
        try:
            query = """
            MATCH (b:Belief {uid: $belief_uid})-[:HAS_CHANGE]->(c:BeliefChange)
            RETURN c
            ORDER BY c.timestamp ASC
            """

            params = {"belief_uid": belief_uid}

            results = db.execute_query(query, params, fetch_all=True)

            timeline = []
            for result in results:
                if "c" in result:
                    timeline.append(dict(result["c"]))

            return timeline
        except Exception as e:
            logger.error(f"Error getting belief change timeline: {str(e)}")
            return []

    def generate_belief_evolution_report(
        self, db: Neo4jConnection, belief_uid: str
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive report on how a belief has evolved.

        Args:
            db: Neo4j connection
            belief_uid: UID of the belief

        Returns:
            Dictionary containing the evolution report
        """
        try:
            # Get the current belief
            belief = self._get_belief(db, belief_uid)
            if not belief:
                return {"error": f"Belief with UID {belief_uid} not found"}

            # Get the belief's change timeline
            timeline = self.get_belief_change_timeline(db, belief_uid)

            # Get the belief's version history
            history = self._get_belief_history(db, belief_uid)

            # Get sources that influenced this belief
            sources = self._get_belief_sources(db, belief_uid)

            # Get related beliefs
            related_beliefs = self._get_related_beliefs(db, belief_uid)

            # Generate confidence history for visualization
            confidence_history = [
                {
                    "version": v.get("version"),
                    "confidence": v.get("confidence", 0),
                    "timestamp": v.get("timestamp"),
                }
                for v in history
            ]

            # Generate natural language summary
            summary = self._generate_evolution_summary(
                belief, timeline, history, sources
            )

            return {
                "belief": belief,
                "timeline": timeline,
                "confidence_history": confidence_history,
                "sources": sources,
                "related_beliefs": related_beliefs,
                "summary": summary,
            }
        except Exception as e:
            logger.error(f"Error generating belief evolution report: {str(e)}")
            return {"error": str(e)}

    def _get_related_beliefs(
        self, db: Neo4jConnection, belief_uid: str
    ) -> List[Dict[str, Any]]:
        """
        Get beliefs related to the given belief.

        Args:
            db: Neo4j connection
            belief_uid: UID of the belief

        Returns:
            List of related beliefs with relationship details
        """
        query = """
        MATCH (b:Belief {uid: $belief_uid})-[r]-(related:Belief)
        RETURN related, type(r) as relationship_type
        """

        params = {"belief_uid": belief_uid}

        results = db.execute_query(query, params, fetch_all=True)

        related = []
        for result in results:
            if "related" in result:
                belief_data = dict(result["related"])
                belief_data["relationship"] = result.get("relationship_type")
                related.append(belief_data)

        return related

    def _generate_evolution_summary(
        self,
        belief: Dict[str, Any],
        timeline: List[Dict[str, Any]],
        history: List[Dict[str, Any]],
        sources: List[Dict[str, Any]],
    ) -> str:
        """
        Generate a summary of how a belief has evolved over time.

        Args:
            belief: Current belief data
            timeline: List of change records
            history: List of historical versions of the belief
            sources: List of sources that influenced the belief

        Returns:
            Natural language summary of belief evolution
        """
        if not history or len(history) < 2:
            return f"This belief '{belief.get('statement')}' has remained stable since its creation."

        # Start with a summary
        summary = [
            f"Evolution of Belief: '{belief.get('statement')}'",
            f"Current confidence: {belief.get('confidence', 0):.2f}",
            f"Created: {history[0].get('timestamp')}",
            f"Last updated: {history[-1].get('timestamp')}",
            f"Number of updates: {len(history) - 1}",
            "",
        ]

        # Confidence trend
        initial_confidence = history[0].get("confidence", 0)
        current_confidence = belief.get("confidence", 0)
        confidence_delta = current_confidence - initial_confidence

        if abs(confidence_delta) < 0.05:
            summary.append("Confidence has remained relatively stable over time.")
        elif confidence_delta > 0:
            summary.append(
                f"Confidence has increased by {confidence_delta:.2f} since creation."
            )
        else:
            summary.append(
                f"Confidence has decreased by {abs(confidence_delta):.2f} since creation."
            )

        # Statement evolution
        initial_statement = history[0].get("statement", "")
        if initial_statement != belief.get("statement", ""):
            summary.append(
                f"The belief statement has evolved from '{initial_statement}' to its current form."
            )

        # Key turning points
        if timeline:
            significant_changes = [
                change
                for change in timeline
                if change.get("change_type")
                in [ChangeType.PARADIGM_SHIFT.value, ChangeType.DOMAIN_SHIFT.value]
                or abs(
                    change.get("current_confidence", 0)
                    - change.get("previous_confidence", 0)
                )
                > 0.2
            ]

            if significant_changes:
                summary.append("\nKey turning points in belief evolution:")
                for change in significant_changes:
                    timestamp = change.get("timestamp", "unknown time")
                    change_type = change.get("change_type", "unknown")
                    reason = change.get("reason", "No reason provided")

                    summary.append(
                        f"• {timestamp}: {change_type.replace('_', ' ').title()}"
                    )
                    summary.append(f"  Reason: {reason}")

        # Source influence
        if sources:
            top_sources = sorted(
                sources, key=lambda s: s.get("confidence_contribution", 0), reverse=True
            )[:3]

            summary.append("\nMost influential sources:")
            for source in top_sources:
                contribution = source.get("confidence_contribution", 0)
                summary.append(
                    f"• {source.get('name', 'Unknown source')}: contributed {contribution:.2f} to confidence"
                )

        return "\n".join(summary)
