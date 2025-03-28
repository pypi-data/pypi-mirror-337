"""
Opinion Balance Monitoring Module for SynapseGraph.

This module handles the monitoring and analysis of opinion balance in the knowledge graph,
including:
1. Tracking opinion stance distributions across topics
2. Detecting potential bias in the knowledge base
3. Creating BalanceAudit nodes to record balance metrics
4. Providing recommendations for addressing imbalances
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import math
import json

from synapsegraph_lib.core.config import OpinionStance
from synapsegraph_lib.core.database import Neo4jConnection
from synapsegraph_lib.core.models import Opinion

logger = logging.getLogger(__name__)


class BalanceMonitor:
    """
    Monitors and analyzes opinion balance in the knowledge graph.

    This class is responsible for:
    1. Calculating stance distributions across topics
    2. Detecting potential bias in opinions
    3. Creating BalanceAudit nodes to track balance metrics over time
    4. Providing recommendations for addressing imbalances
    """

    def __init__(self, bias_threshold: float = 0.3, min_opinions_for_audit: int = 5):
        """
        Initialize the BalanceMonitor.

        Args:
            bias_threshold: Threshold for considering a topic biased (0.0-1.0)
                            Higher values allow more imbalance before flagging
            min_opinions_for_audit: Minimum number of opinions required to perform an audit
        """
        self.bias_threshold = bias_threshold
        self.min_opinions_for_audit = min_opinions_for_audit

    def analyze_topic_balance(self, db: Neo4jConnection, topic: str) -> Dict[str, Any]:
        """
        Analyze the balance of opinions on a specific topic.

        Args:
            db: Neo4j connection
            topic: Topic to analyze

        Returns:
            Dictionary with balance metrics
        """
        # Get stance distribution for the topic
        distribution = self._get_stance_distribution(db, topic)

        # Calculate balance metrics
        total_opinions = sum(distribution.values())

        if total_opinions < self.min_opinions_for_audit:
            logger.info(f"Not enough opinions on topic '{topic}' for balance analysis")
            return {
                "topic": topic,
                "total_opinions": total_opinions,
                "distribution": distribution,
                "bias_score": 0.0,
                "is_biased": False,
                "dominant_stance": None,
                "timestamp": datetime.now().isoformat(),
                "sufficient_data": False,
            }

        # Calculate percentages
        percentages = {
            stance: count / total_opinions for stance, count in distribution.items()
        }

        # Calculate bias score (how far from equal distribution)
        expected_percentage = 1.0 / len(OpinionStance)
        bias_score = 0.0

        for stance in OpinionStance:
            percentage = percentages.get(stance.value, 0.0)
            bias_score += abs(percentage - expected_percentage)

        # Normalize bias score to 0-1 range
        bias_score = bias_score / 2.0

        # Determine if biased based on threshold
        is_biased = bias_score > self.bias_threshold

        # Find dominant stance
        dominant_stance = (
            max(distribution.items(), key=lambda x: x[1])[0] if distribution else None
        )

        # Create result
        result = {
            "topic": topic,
            "total_opinions": total_opinions,
            "distribution": distribution,
            "percentages": percentages,
            "bias_score": bias_score,
            "is_biased": is_biased,
            "dominant_stance": dominant_stance,
            "timestamp": datetime.now().isoformat(),
            "sufficient_data": True,
        }

        return result

    def _get_stance_distribution(
        self, db: Neo4jConnection, topic: str
    ) -> Dict[str, int]:
        """
        Get the distribution of opinion stances on a specific topic.

        Args:
            db: Neo4j connection
            topic: Topic to analyze

        Returns:
            Dictionary with counts for each stance
        """
        # First try to find opinions linked to a Topic node
        query = """
        MATCH (o:Opinion)-[:ABOUT]->(t:Topic {name: $topic})
        RETURN o.stance AS stance, count(o) AS count
        """

        params = {"topic": topic}

        try:
            results = db.execute_query(query, params, fetch_all=True)

            # Initialize with all stances set to 0
            distribution = {stance.value: 0 for stance in OpinionStance}

            # Update with actual counts
            for result in results:
                stance = result.get("stance")
                count = result.get("count", 0)
                if stance in distribution:
                    distribution[stance] = count

            # If no results, try an alternative approach to find opinions by topic
            if sum(distribution.values()) == 0:
                logger.info(
                    f"No opinions found for topic '{topic}' using direct relationship query, trying metadata search"
                )

                # Try to find opinions with topic in metadata
                query = """
                MATCH (o:Opinion)
                WHERE o.metadata CONTAINS $topic_json
                RETURN o.stance AS stance, count(o) AS count
                """

                params = {"topic_json": f'"topic":"{topic}"'}
                results = db.execute_query(query, params, fetch_all=True)

                # Update with actual counts
                for result in results:
                    stance = result.get("stance")
                    count = result.get("count", 0)
                    if stance in distribution:
                        distribution[stance] = count

            return distribution
        except Exception as e:
            logger.error(f"Error getting stance distribution: {str(e)}")
            return {stance.value: 0 for stance in OpinionStance}

    def create_balance_audit(self, db: Neo4jConnection, topic: str) -> Optional[str]:
        """
        Create a balance audit for a specific topic.

        Args:
            db: Neo4j connection
            topic: Topic to audit

        Returns:
            UID of the created audit, or None if creation failed or insufficient data
        """
        # Analyze topic balance
        balance_data = self.analyze_topic_balance(db, topic)

        # Check if we have sufficient data
        if not balance_data.get("sufficient_data", False):
            logger.info(f"Not enough opinions on topic '{topic}' for balance analysis")
            return None

        # Create audit node
        audit_uid = self._create_audit_node(db, balance_data)
        if not audit_uid:
            logger.error(f"Failed to create balance audit for topic: {topic}")
            return None

        # Link audit to topic
        if not self._link_audit_to_topic(db, audit_uid, topic):
            logger.error(f"Failed to link audit to topic: {topic}")
            return None

        # Generate recommendations
        recommendations = self.generate_balance_recommendations(balance_data)

        # Update audit with recommendations
        if recommendations:
            self._update_audit_recommendations(db, audit_uid, recommendations)

        logger.info(f"Created balance audit for topic: {topic}")
        return audit_uid

    def _create_audit_node(
        self, db: Neo4jConnection, balance_data: Dict[str, Any]
    ) -> Optional[str]:
        """
        Create a BalanceAudit node in the database.

        Args:
            db: Neo4j connection
            balance_data: Balance analysis data

        Returns:
            UID of the created node, or None if creation failed
        """
        # Generate a unique ID for the audit
        from uuid import uuid4

        audit_uid = str(uuid4())

        query = """
        CREATE (a:BalanceAudit {
            uid: $uid,
            topic: $topic,
            timestamp: datetime($timestamp),
            total_opinions: $total_opinions,
            bias_score: $bias_score,
            is_biased: $is_biased,
            dominant_stance: $dominant_stance,
            distribution: $distribution,
            recommendations: $recommendations
        })
        RETURN a.uid as uid
        """

        params = {
            "uid": audit_uid,
            "topic": balance_data["topic"],
            "timestamp": balance_data["timestamp"],
            "total_opinions": balance_data["total_opinions"],
            "bias_score": balance_data["bias_score"],
            "is_biased": balance_data["is_biased"],
            "dominant_stance": balance_data["dominant_stance"] or "",
            "distribution": json.dumps(balance_data["distribution"]),
            "recommendations": json.dumps([]),  # Will be updated later if needed
        }

        try:
            result = db.execute_query(query, params)
            return audit_uid if result else None
        except Exception as e:
            logger.error(f"Error creating balance audit node: {str(e)}")
            return None

    def _link_audit_to_topic(
        self, db: Neo4jConnection, audit_uid: str, topic: str
    ) -> bool:
        """
        Link a BalanceAudit node to a Topic node.

        Args:
            db: Neo4j connection
            audit_uid: UID of the BalanceAudit node
            topic: Topic name

        Returns:
            True if successful, False otherwise
        """
        query = """
        MATCH (a:BalanceAudit {uid: $audit_uid})
        MERGE (t:Topic {name: $topic})
        MERGE (a)-[:AUDITS]->(t)
        RETURN a, t
        """

        params = {"audit_uid": audit_uid, "topic": topic}

        try:
            results = db.execute_query(query, params, fetch_all=True)
            return len(results) > 0
        except Exception as e:
            logger.error(f"Error linking audit to topic: {str(e)}")
            return False

    def _update_audit_recommendations(
        self, db: Neo4jConnection, audit_uid: str, recommendations: List[str]
    ) -> bool:
        """
        Update the recommendations field of a BalanceAudit node.

        Args:
            db: Neo4j connection
            audit_uid: UID of the BalanceAudit node
            recommendations: List of recommendation strings

        Returns:
            True if successful, False otherwise
        """
        query = """
        MATCH (a:BalanceAudit {uid: $audit_uid})
        SET a.recommendations = $recommendations
        RETURN a
        """

        params = {
            "audit_uid": audit_uid,
            "recommendations": json.dumps(recommendations),
        }

        try:
            result = db.execute_query(query, params)
            return bool(result)
        except Exception as e:
            logger.error(f"Error updating balance audit recommendations: {str(e)}")
            return False

    def generate_balance_recommendations(
        self, balance_data: Dict[str, Any]
    ) -> List[str]:
        """
        Generate recommendations for addressing opinion imbalance.

        Args:
            balance_data: Balance analysis data

        Returns:
            List of recommendation strings
        """
        recommendations = []

        if not balance_data["is_biased"]:
            return ["No significant bias detected. Continue monitoring."]

        # Get the dominant and underrepresented stances
        dominant_stance = balance_data["dominant_stance"]
        percentages = balance_data["percentages"]

        underrepresented = []
        for stance, percentage in percentages.items():
            if percentage < 0.2:  # Less than 20% representation
                underrepresented.append(stance)

        # Generate recommendations based on the imbalance
        if dominant_stance:
            recommendations.append(
                f"The topic '{balance_data['topic']}' shows a bias toward '{dominant_stance}' opinions "
                f"(bias score: {balance_data['bias_score']:.2f})."
            )

        if underrepresented:
            stances_str = ", ".join([f"'{stance}'" for stance in underrepresented])
            recommendations.append(
                f"Consider seeking more {stances_str} perspectives on this topic."
            )

        recommendations.append(
            "Consider using more diverse sources when gathering information on this topic."
        )

        if balance_data["total_opinions"] < 10:
            recommendations.append(
                "The total number of opinions is relatively low. Consider gathering more opinions "
                "to ensure a comprehensive understanding of the topic."
            )

        return recommendations

    def get_recent_audits(
        self, db: Neo4jConnection, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get the most recent balance audits.

        Args:
            db: Neo4j connection
            limit: Maximum number of audits to return

        Returns:
            List of audit data dictionaries
        """
        query = """
        MATCH (a:BalanceAudit)
        RETURN a
        ORDER BY a.timestamp DESC
        LIMIT $limit
        """

        params = {"limit": limit}

        try:
            results = db.execute_query(query, params, fetch_all=True)

            audits = []
            for result in results:
                audit_data = dict(result["a"])

                # Parse JSON fields
                if "distribution" in audit_data:
                    audit_data["distribution"] = json.loads(audit_data["distribution"])

                if "recommendations" in audit_data:
                    audit_data["recommendations"] = json.loads(
                        audit_data["recommendations"]
                    )

                audits.append(audit_data)

            return audits
        except Exception as e:
            logger.error(f"Error getting recent balance audits: {str(e)}")
            return []

    def get_topic_audit_history(
        self, db: Neo4jConnection, topic: str
    ) -> List[Dict[str, Any]]:
        """
        Get the audit history for a specific topic.

        Args:
            db: Neo4j connection
            topic: Topic to get audit history for

        Returns:
            List of audit data dictionaries in chronological order
        """
        query = """
        MATCH (a:BalanceAudit)
        WHERE a.topic = $topic
        RETURN a
        ORDER BY a.timestamp ASC
        """

        params = {"topic": topic}

        try:
            results = db.execute_query(query, params, fetch_all=True)

            audits = []
            for result in results:
                audit_data = dict(result["a"])

                # Parse JSON fields
                if "distribution" in audit_data and isinstance(
                    audit_data["distribution"], str
                ):
                    try:
                        audit_data["distribution"] = json.loads(
                            audit_data["distribution"]
                        )
                    except json.JSONDecodeError:
                        logger.warning(
                            f"Failed to parse distribution for audit: {audit_data.get('uid')}"
                        )

                if "recommendations" in audit_data and isinstance(
                    audit_data["recommendations"], str
                ):
                    try:
                        audit_data["recommendations"] = json.loads(
                            audit_data["recommendations"]
                        )
                    except json.JSONDecodeError:
                        logger.warning(
                            f"Failed to parse recommendations for audit: {audit_data.get('uid')}"
                        )

                audits.append(audit_data)

            return audits
        except Exception as e:
            logger.error(f"Error getting topic audit history: {str(e)}")
            return []

    def get_most_biased_topics(
        self, db: Neo4jConnection, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get the most biased topics based on the most recent audits.

        Args:
            db: Neo4j connection
            limit: Maximum number of topics to return

        Returns:
            List of topic data dictionaries with bias scores
        """
        query = """
        MATCH (a:BalanceAudit)
        WITH a.topic AS topic, a
        ORDER BY a.timestamp DESC
        WITH topic, collect(a)[0] AS latest_audit
        WHERE latest_audit.is_biased = true
        RETURN topic, latest_audit.bias_score AS bias_score, latest_audit.dominant_stance AS dominant_stance
        ORDER BY bias_score DESC
        LIMIT $limit
        """

        params = {"limit": limit}

        try:
            results = db.execute_query(query, params, fetch_all=True)

            biased_topics = []
            for result in results:
                biased_topics.append(
                    {
                        "topic": result["topic"],
                        "bias_score": result["bias_score"],
                        "dominant_stance": result["dominant_stance"],
                    }
                )

            return biased_topics
        except Exception as e:
            logger.error(f"Error getting most biased topics: {str(e)}")
            return []

    def audit_all_topics(
        self, db: Neo4jConnection, min_opinions: int = 5
    ) -> Dict[str, Any]:
        """
        Perform balance audits on all topics with sufficient opinions.

        Args:
            db: Neo4j connection
            min_opinions: Minimum number of opinions required to audit a topic

        Returns:
            Dictionary with audit results summary
        """
        # Get all topics with their opinion counts
        topics = self._get_topics_with_opinion_counts(db)

        # Filter topics with sufficient opinions
        eligible_topics = [topic for topic, count in topics if count >= min_opinions]

        logger.info(f"Found {len(eligible_topics)} topics eligible for balance audit")

        # Perform audits
        audit_results = {
            "total_topics": len(topics),
            "total_topics_audited": len(eligible_topics),
            "audited_topics": len(eligible_topics),
            "biased_topics": 0,
            "biased_topics_count": 0,
            "created_audits": 0,
            "topics": [],
        }

        for topic in eligible_topics:
            audit_uid = self.create_balance_audit(db, topic)

            if audit_uid:
                audit_results["created_audits"] += 1

                # Get the audit data to check if biased
                balance_data = self.analyze_topic_balance(db, topic)

                if balance_data["is_biased"]:
                    audit_results["biased_topics"] += 1
                    audit_results["biased_topics_count"] += 1

                audit_results["topics"].append(
                    {
                        "topic": topic,
                        "audit_uid": audit_uid,
                        "is_biased": balance_data["is_biased"],
                        "bias_score": balance_data["bias_score"],
                    }
                )

        return audit_results

    def _get_topics_with_opinion_counts(
        self, db: Neo4jConnection
    ) -> List[Dict[str, Any]]:
        """
        Get all topics with their opinion counts.

        Args:
            db: Neo4j connection

        Returns:
            List of dictionaries with 'topic' and 'opinion_count' keys
        """
        # Get all opinions
        query = """
        MATCH (o:Opinion)
        RETURN o
        """

        try:
            results = db.execute_query(query, {}, fetch_all=True)

            # Process opinions to extract topics from metadata
            topic_counts = {}

            for result in results:
                opinion_data = dict(result["o"])
                metadata_str = opinion_data.get("metadata", "{}")

                try:
                    if isinstance(metadata_str, str):
                        metadata = json.loads(metadata_str)
                    else:
                        metadata = metadata_str

                    topic = metadata.get("topic")
                    if topic:
                        topic_counts[topic] = topic_counts.get(topic, 0) + 1
                except json.JSONDecodeError:
                    logger.warning(
                        f"Failed to parse metadata for opinion: {opinion_data.get('uid')}"
                    )
                    continue

            # Convert to list of dictionaries and sort by count
            topic_list = [
                {"topic": topic, "opinion_count": count}
                for topic, count in topic_counts.items()
            ]
            topic_list.sort(key=lambda x: x["opinion_count"], reverse=True)

            return topic_list
        except Exception as e:
            logger.error(f"Error getting topics with opinion counts: {str(e)}")
            return []
