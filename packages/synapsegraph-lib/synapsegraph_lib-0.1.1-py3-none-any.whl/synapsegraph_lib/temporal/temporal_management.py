"""
Temporal Knowledge Management Module for SynapseGraph.

This module handles the temporal aspects of knowledge in the graph, including:
1. Confidence decay over time for beliefs and opinions
2. Time horizon tracking for opinions
3. Temporal relevance scoring
"""

import logging
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
import math
import json
import neo4j

from synapsegraph_lib.core.config import TimeHorizon, OpinionStance
from synapsegraph_lib.core.database import Neo4jConnection
from synapsegraph_lib.core.models import Opinion, Belief

logger = logging.getLogger(__name__)


class TemporalManager:
    """
    Manages temporal aspects of knowledge in the graph.

    This class is responsible for:
    1. Applying confidence decay to beliefs and opinions over time
    2. Tracking and updating time horizons for opinions
    3. Calculating temporal relevance scores
    """

    def __init__(self):
        """Initialize the TemporalManager with default decay rates."""
        # Base decay rates by time horizon
        self.decay_rates = {
            TimeHorizon.SHORT_TERM: 0.05,  # Fast decay for short-term opinions
            TimeHorizon.MEDIUM_TERM: 0.03,  # Medium decay for medium-term opinions
            TimeHorizon.LONG_TERM: 0.01,  # Slow decay for long-term opinions
            TimeHorizon.UNKNOWN: 0.03,  # Default to medium decay rate
        }

        # Domain-specific decay rates for beliefs
        self.domain_decay_rates = {
            "scientific_fact": 0.01,  # Very slow decay for scientific facts
            "historical_event": 0.02,  # Slow decay for historical events
            "current_event": 0.05,  # Fast decay for current events
            "technology_trend": 0.04,  # Medium-fast decay for tech trends
            "social_trend": 0.04,  # Medium-fast decay for social trends
            "opinion_poll": 0.06,  # Very fast decay for opinion polls
            "evergreen": 0.01,  # Very slow decay for evergreen content
            "speculative": 0.05,  # Fast decay for speculative content
        }

        # Default decay rate for beliefs
        self.decay_rate = 0.03

        # Time horizons in days
        self.short_term_days = 30
        self.medium_term_days = 90
        self.long_term_days = 365

    def _convert_to_datetime(self, dt_obj: Any) -> datetime:
        """
        Convert various datetime formats to Python datetime.
        Ensures all datetimes are naive (without timezone info) for consistent comparison.

        Args:
            dt_obj: Object to convert (string, Neo4j DateTime, or datetime)

        Returns:
            Python datetime object (naive, without timezone)
        """
        if dt_obj is None:
            return datetime.now()

        if isinstance(dt_obj, datetime):
            # Remove timezone info if present
            if dt_obj.tzinfo is not None:
                return dt_obj.replace(tzinfo=None)
            return dt_obj

        elif isinstance(dt_obj, str):
            try:
                # Parse ISO format string, then remove timezone
                dt = datetime.fromisoformat(dt_obj.replace("Z", "+00:00"))
                return dt.replace(tzinfo=None)
            except ValueError:
                # Fall back to current time if parsing fails
                logger.warning(f"Could not parse datetime string: {dt_obj}")
                return datetime.now()

        elif hasattr(dt_obj, "to_native"):  # Neo4j DateTime object
            native_dt = dt_obj.to_native()
            # Remove timezone if present
            if hasattr(native_dt, "tzinfo") and native_dt.tzinfo is not None:
                return native_dt.replace(tzinfo=None)
            return native_dt

        else:
            logger.warning(f"Unsupported datetime format: {type(dt_obj)}")
            return datetime.now()

    def apply_confidence_decay(self, db: Neo4jConnection) -> int:
        """
        Apply confidence decay to all beliefs and opinions based on their age.

        Args:
            db: Neo4j connection

        Returns:
            Number of nodes updated
        """
        # Get current time
        current_time = datetime.now()

        # Apply decay to beliefs
        belief_count = self._decay_beliefs(db, current_time)

        # Apply decay to opinions
        opinion_count = self._decay_opinions(db, current_time)

        total_updated = belief_count + opinion_count
        logger.info(f"Applied confidence decay to {total_updated} nodes")
        return total_updated

    def _decay_beliefs(self, db: Neo4jConnection, current_time: datetime) -> int:
        """
        Apply confidence decay to beliefs.

        Args:
            db: Neo4j connection
            current_time: Current time

        Returns:
            Number of beliefs updated
        """
        query = """
        MATCH (b:Belief)
        WHERE b.created_at IS NOT NULL
        WITH b, datetime(b.created_at) AS creation_time
        WITH b, duration.between(creation_time, datetime($current_time)) AS age_duration
        WITH b, age_duration.days / 365.0 AS age_years, b.category AS category
        WHERE b.confidence > 0.1  // Don't decay beliefs that are already very low confidence
        
        // Apply domain-specific decay based on category
        WITH b, age_years, category,
             CASE 
                WHEN category = 'scientific_fact' THEN $scientific_fact_rate
                WHEN category = 'historical_event' THEN $historical_event_rate
                WHEN category = 'current_event' THEN $current_event_rate
                WHEN category = 'technology_trend' THEN $technology_trend_rate
                WHEN category = 'social_trend' THEN $social_trend_rate
                WHEN category = 'opinion_poll' THEN $opinion_poll_rate
                WHEN category = 'evergreen' THEN $evergreen_rate
                WHEN category = 'speculative' THEN $speculative_rate
                ELSE $default_decay_rate
             END AS decay_rate
             
        SET b.confidence = b.confidence * (1.0 - $decay_rate * age_years)
        SET b.confidence = CASE WHEN b.confidence < 0.1 THEN 0.1 ELSE b.confidence END
        SET b.updated_at = $current_time
        RETURN count(b) AS updated_count
        """

        params = {
            "current_time": current_time.isoformat(),
            "decay_rate": self.decay_rate,
            "default_decay_rate": self.decay_rate,
            "scientific_fact_rate": self.domain_decay_rates["scientific_fact"],
            "historical_event_rate": self.domain_decay_rates["historical_event"],
            "current_event_rate": self.domain_decay_rates["current_event"],
            "technology_trend_rate": self.domain_decay_rates["technology_trend"],
            "social_trend_rate": self.domain_decay_rates["social_trend"],
            "opinion_poll_rate": self.domain_decay_rates["opinion_poll"],
            "evergreen_rate": self.domain_decay_rates["evergreen"],
            "speculative_rate": self.domain_decay_rates["speculative"],
        }

        try:
            result = db.execute_query(query, params, fetch_all=True)
            if result and len(result) > 0:
                return result[0]["updated_count"]
            return 0
        except Exception as e:
            logger.error(f"Error applying confidence decay to beliefs: {str(e)}")
            return 0

    def _decay_opinions(self, db: Neo4jConnection, current_time: datetime) -> int:
        """
        Apply confidence decay to all opinions based on their age.

        Args:
            db: Neo4j connection
            current_time: Current time

        Returns:
            Number of opinions updated
        """
        # Get all opinions that need decay
        query = """
        MATCH (o:Opinion)
        WHERE o.confidence > 0.1
        RETURN o
        """

        with db.session() as session:
            result = session.run(query)
            opinions = list(result)

            updated_count = 0
            for record in opinions:
                try:
                    opinion = record["o"]
                    opinion_dict = dict(opinion.items())

                    # Convert time horizon and stance from strings to enums
                    try:
                        time_horizon = TimeHorizon[
                            opinion_dict.get("time_horizon", "UNKNOWN")
                        ]
                    except (KeyError, ValueError):
                        time_horizon = TimeHorizon.UNKNOWN

                    try:
                        stance = OpinionStance[opinion_dict.get("stance", "NEUTRAL")]
                    except (KeyError, ValueError):
                        stance = OpinionStance.NEUTRAL

                    # Parse metadata if it's a string
                    try:
                        metadata = (
                            json.loads(opinion_dict.get("metadata", "{}"))
                            if isinstance(opinion_dict.get("metadata"), str)
                            else opinion_dict.get("metadata", {})
                        )
                    except json.JSONDecodeError:
                        metadata = {}

                    # Calculate days since last update - use _convert_to_datetime instead of manual conversion
                    updated_at = self._convert_to_datetime(
                        opinion_dict.get("updated_at")
                    )
                    days_since_update = (current_time - updated_at).days

                    # Calculate decay based on time horizon
                    decay_rate = self.get_opinion_decay_rate(time_horizon)

                    # Apply resistance factor
                    resistance_factor = opinion_dict.get("resistance_factor", 1.0)
                    effective_decay_rate = decay_rate * (1.0 - resistance_factor)

                    # Use multiplicative decay model for consistency with _decay_beliefs
                    old_confidence = float(opinion_dict.get("confidence", 0.0))
                    total_decay_factor = (
                        effective_decay_rate * days_since_update / 365.0
                    )  # Convert to years for consistency
                    new_confidence = max(
                        0.1, old_confidence * (1.0 - total_decay_factor)
                    )

                    # Record decay in metadata
                    metadata["decay_history"] = metadata.get("decay_history", [])
                    metadata["decay_history"].append(
                        {
                            "date": current_time.isoformat(),
                            "days_since_update": days_since_update,
                            "decay_rate": decay_rate,
                            "effective_decay_rate": effective_decay_rate,
                            "total_decay_factor": total_decay_factor,
                            "resistance_factor": resistance_factor,
                            "old_confidence": old_confidence,
                            "new_confidence": new_confidence,
                            "decay_model": "multiplicative",
                        }
                    )

                    # Create update query
                    update_query = """
                    MATCH (o:Opinion)
                    WHERE id(o) = $opinion_id
                    SET o.confidence = $new_confidence,
                        o.version = o.version + 1,
                        o.updated_by = 'temporal_decay',
                        o.last_updated = $current_time,
                        o.metadata = $metadata
                    """

                    session.run(
                        update_query,
                        opinion_id=opinion.id,
                        new_confidence=new_confidence,
                        current_time=current_time,
                        metadata=metadata,
                    )

                    updated_count += 1

                except Exception as e:
                    logger.error(f"Error applying decay to opinion: {str(e)}")
                    continue

            return updated_count

    def update_time_horizons(self, db: Neo4jConnection) -> int:
        """
        Update time horizons for opinions based on their content and supporting beliefs.

        Args:
            db: Neo4j connection

        Returns:
            Number of opinions updated
        """
        # First, identify opinions that need time horizon updates
        opinions_to_update = self._identify_opinions_for_horizon_update(db)

        if not opinions_to_update:
            logger.info("No opinions need time horizon updates")
            return 0

        # Update the time horizons
        updated_count = 0
        for opinion in opinions_to_update:
            new_horizon = self._determine_time_horizon(db, opinion)
            if new_horizon and new_horizon != opinion.time_horizon:
                updated = self._update_opinion_time_horizon(
                    db, opinion.uid, new_horizon
                )
                if updated:
                    updated_count += 1

        logger.info(f"Updated time horizons for {updated_count} opinions")
        return updated_count

    def _identify_opinions_for_horizon_update(
        self, db: Neo4jConnection
    ) -> List[Opinion]:
        """
        Identify opinions that need their time horizons updated.

        Args:
            db: Neo4j connection

        Returns:
            List of opinions that need updates
        """
        query = """
        MATCH (o:Opinion)
        WHERE o.time_horizon IS NULL OR o.time_horizon = 'Unknown'
        OR NOT EXISTS(o.time_horizon_updated_at)
        OR datetime(o.time_horizon_updated_at) < datetime() - duration({days: 30})
        RETURN o
        """

        try:
            results = db.execute_query(query, {}, fetch_all=True)
            return [Opinion.from_dict(dict(result["o"])) for result in results]
        except Exception as e:
            logger.error(f"Error identifying opinions for horizon update: {str(e)}")
            return []

    def _determine_time_horizon(
        self, db: Neo4jConnection, opinion: Opinion
    ) -> Optional[TimeHorizon]:
        """
        Determine the appropriate time horizon for an opinion.

        Args:
            db: Neo4j connection
            opinion: Opinion to analyze

        Returns:
            Appropriate TimeHorizon value
        """
        # First, check if we can determine from the statement using LLM
        horizon_from_statement = self._analyze_statement_for_horizon(opinion.statement)

        # Then, check the supporting beliefs
        horizon_from_beliefs = self._analyze_beliefs_for_horizon(db, opinion)

        # If both methods yield a result, take the longer-term one
        if horizon_from_statement and horizon_from_beliefs:
            return self._get_longer_horizon(
                horizon_from_statement, horizon_from_beliefs
            )

        # Otherwise, return whichever one we have
        return horizon_from_statement or horizon_from_beliefs or TimeHorizon.UNKNOWN

    def _analyze_statement_for_horizon(self, statement: str) -> Optional[TimeHorizon]:
        """
        Analyze an opinion statement to determine its time horizon.

        Args:
            statement: Opinion statement

        Returns:
            TimeHorizon value based on statement analysis
        """
        # Look for time-related keywords in the statement
        statement_lower = statement.lower()

        # Check for explicit time indicators
        if any(
            term in statement_lower
            for term in ["today", "now", "current", "immediate", "week", "month"]
        ):
            return TimeHorizon.SHORT_TERM

        if any(term in statement_lower for term in ["year", "annual", "decade"]):
            return TimeHorizon.MEDIUM_TERM

        if any(
            term in statement_lower
            for term in ["century", "permanent", "forever", "always", "never"]
        ):
            return TimeHorizon.LONG_TERM

        # TODO: Implement LLM-based analysis for more sophisticated time horizon detection
        # This is a placeholder for future work. Currently uses only keyword matching.
        # A more sophisticated approach would use an LLM to analyze semantic time references.
        return None

    def _analyze_beliefs_for_horizon(
        self, db: Neo4jConnection, opinion: Opinion
    ) -> Optional[TimeHorizon]:
        """
        Analyze the supporting beliefs of an opinion to determine its time horizon.

        Args:
            db: Neo4j connection
            opinion: Opinion to analyze

        Returns:
            TimeHorizon value based on supporting beliefs
        """
        query = """
        MATCH (o:Opinion {uid: $opinion_uid})<-[:SUPPORTS]-(b:Belief)
        RETURN b
        """

        params = {"opinion_uid": opinion.uid}

        try:
            results = db.execute_query(query, params, fetch_all=True)
            beliefs = [Belief.from_dict(dict(result["b"])) for result in results]

            if not beliefs:
                return None

            # Analyze the beliefs to determine time horizon
            # For now, use a simple heuristic based on the average age of beliefs
            total_age = 0
            for belief in beliefs:
                if belief.created_at:
                    created_at = datetime.fromisoformat(belief.created_at)
                    age_days = (datetime.now() - created_at).days
                    total_age += age_days

            avg_age = total_age / len(beliefs)

            # Determine horizon based on average age
            if avg_age < self.short_term_days:
                return TimeHorizon.SHORT_TERM
            elif avg_age < self.medium_term_days:
                return TimeHorizon.MEDIUM_TERM
            else:
                return TimeHorizon.LONG_TERM

        except Exception as e:
            logger.error(f"Error analyzing beliefs for horizon: {str(e)}")
            return None

    def _get_longer_horizon(
        self, horizon1: TimeHorizon, horizon2: TimeHorizon
    ) -> TimeHorizon:
        """
        Get the longer of two time horizons.

        Args:
            horizon1: First time horizon
            horizon2: Second time horizon

        Returns:
            Longer time horizon
        """
        horizon_order = {
            TimeHorizon.UNKNOWN: 0,
            TimeHorizon.SHORT_TERM: 1,
            TimeHorizon.MEDIUM_TERM: 2,
            TimeHorizon.LONG_TERM: 3,
        }

        return (
            horizon1 if horizon_order[horizon1] >= horizon_order[horizon2] else horizon2
        )

    def _update_opinion_time_horizon(
        self, db: Neo4jConnection, opinion_uid: str, time_horizon: TimeHorizon
    ) -> bool:
        """
        Update the time horizon of an opinion.

        Args:
            db: Neo4j connection
            opinion_uid: UID of the opinion to update
            time_horizon: New time horizon value

        Returns:
            True if successful, False otherwise
        """
        query = """
        MATCH (o:Opinion {uid: $opinion_uid})
        SET o.time_horizon = $time_horizon
        SET o.time_horizon_updated_at = $updated_at
        RETURN o
        """

        params = {
            "opinion_uid": opinion_uid,
            "time_horizon": time_horizon.value,
            "updated_at": datetime.now().isoformat(),
        }

        try:
            db.execute_query(query, params)
            logger.info(
                f"Updated time horizon for opinion {opinion_uid} to {time_horizon.value}"
            )
            return True
        except Exception as e:
            logger.error(f"Error updating opinion time horizon: {str(e)}")
            return False

    def calculate_temporal_relevance(
        self, db: Neo4jConnection, topic: str
    ) -> List[Dict[str, Any]]:
        """
        Calculate temporal relevance scores for opinions on a given topic.

        Args:
            db: Neo4j connection
            topic: Topic to analyze

        Returns:
            List of opinions with their temporal relevance scores
        """
        query = """
        MATCH (o:Opinion)-[:ABOUT]->(t:Topic {name: $topic})
        WHERE o.created_at IS NOT NULL
        WITH o, datetime(o.created_at) AS creation_time
        WITH o, duration.between(creation_time, datetime()) AS age_duration
        WITH o, age_duration.days AS age_days
        
        // Calculate base temporal relevance score (newer = more relevant)
        WITH o, 
             CASE 
                WHEN age_days < $short_term_days THEN 1.0
                WHEN age_days < $medium_term_days THEN 0.7
                ELSE 0.4
             END AS base_relevance
        
        // Adjust based on time horizon (longer horizon = more durable relevance)
        WITH o, base_relevance,
             CASE o.time_horizon
                WHEN 'Short-term' THEN 0.8
                WHEN 'Medium-term' THEN 1.0
                WHEN 'Long-term' THEN 1.2
                ELSE 1.0
             END AS horizon_factor
        
        // Calculate final temporal relevance score
        WITH o, base_relevance * horizon_factor AS temporal_relevance
        
        RETURN o.uid AS uid, o.statement AS statement, o.confidence AS confidence, 
               o.time_horizon AS time_horizon, temporal_relevance
        ORDER BY temporal_relevance DESC
        """

        params = {
            "topic": topic,
            "short_term_days": self.short_term_days,
            "medium_term_days": self.medium_term_days,
        }

        try:
            results = db.execute_query(query, params, fetch_all=True)
            return [dict(result) for result in results]
        except Exception as e:
            logger.error(f"Error calculating temporal relevance: {str(e)}")
            return []

    def get_temporal_distribution(self, db: Neo4jConnection) -> Dict[str, int]:
        """
        Get the distribution of opinions across different time horizons.

        Args:
            db: Neo4j connection

        Returns:
            Dictionary with counts for each time horizon (Short-term, Medium-term, Long-term, Unknown)
        """
        # Initialize distribution with proper time horizon values
        distribution = {
            TimeHorizon.SHORT_TERM.value: 0,
            TimeHorizon.MEDIUM_TERM.value: 0,
            TimeHorizon.LONG_TERM.value: 0,
            TimeHorizon.UNKNOWN.value: 0,
        }

        query = """
        MATCH (o:Opinion)
        WHERE o.time_horizon IS NOT NULL
        RETURN o.time_horizon AS horizon, count(o) AS count
        """

        try:
            results = db.execute_query(query, {}, fetch_all=True)

            if not results:
                logger.warning("No opinions found with time horizons")
                return distribution

            for result in results:
                horizon = result.get("horizon")
                count = result.get("count", 0)

                # Validate the horizon value
                if horizon in TimeHorizon._value2member_map_:
                    distribution[horizon] = count
                else:
                    logger.warning(f"Invalid time horizon value found: {horizon}")
                    distribution[TimeHorizon.UNKNOWN.value] += count

            return distribution

        except Exception as e:
            logger.error(f"Error getting temporal distribution: {str(e)}")
            return distribution

    def apply_domain_specific_decay_to_belief(
        self, db: Neo4jConnection, belief: Belief, future_time: datetime
    ) -> Tuple[Belief, float]:
        """
        Apply domain-specific temporal decay to a belief.

        Args:
            db: Neo4j connection
            belief: Belief to apply decay to
            future_time: Future time point

        Returns:
            Tuple of (decayed_belief, decay_amount)
        """
        try:
            # Convert string timestamps to datetime objects if needed
            created_at = belief.created_at
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))

            # Calculate days since creation
            try:
                if isinstance(future_time, str):
                    future_time = datetime.fromisoformat(
                        future_time.replace("Z", "+00:00")
                    )
                days_since_creation = (future_time - created_at).days
            except TypeError:
                # Handle case where one might be a Neo4j DateTime
                # Convert both to timestamps and calculate difference in days
                created_ts = (
                    created_at.timestamp() if hasattr(created_at, "timestamp") else 0
                )
                future_ts = (
                    future_time.timestamp() if hasattr(future_time, "timestamp") else 0
                )
                days_since_creation = int((future_ts - created_ts) / (24 * 3600))

            # Skip if belief is recent
            if days_since_creation < 7:
                return belief, 0.0

            # Base decay rate adjusted by domain characteristics
            base_decay_rate = self.domain_decay_rates.get(belief.category, 0.01)

            # Adjust decay rate based on belief metadata
            if belief.metadata and "evidence_strength" in belief.metadata:
                evidence_strength = belief.metadata["evidence_strength"]
                # Strong evidence reduces decay rate
                if evidence_strength > 0.7:
                    base_decay_rate *= 0.5
                # Weak evidence increases decay rate
                elif evidence_strength < 0.3:
                    base_decay_rate *= 1.5

            # Calculate total decay
            total_decay = min(base_decay_rate * days_since_creation, 0.5)

            # Create a new belief object with decayed confidence (minimum confidence of 0.1)
            decayed_confidence = max(0.1, belief.confidence * (1 - total_decay))

            # Clone the original belief object
            decayed_belief = Belief(
                uid=belief.uid,
                statement=belief.statement,
                confidence=decayed_confidence,  # Use decayed confidence here
                last_updated=datetime.now(),
                expires_at=belief.expires_at,
                version=belief.version + 1,
                category=belief.category,
                speculative=belief.speculative,
                metadata=belief.metadata.copy() if belief.metadata else {},
                created_at=belief.created_at,
            )

            # Record decay in metadata
            if not decayed_belief.metadata:
                decayed_belief.metadata = {}

            decayed_belief.metadata["temporal_decay"] = {
                "days_since_creation": days_since_creation,
                "total_decay": total_decay,
                "original_confidence": belief.confidence,
                "decayed_confidence": decayed_belief.confidence,
                "decay_rate": base_decay_rate,
                "decay_timestamp": datetime.now().isoformat(),
            }

            # Save decayed belief
            decayed_belief.save(db)

            return decayed_belief, total_decay

        except Exception as e:
            logging.error(f"Error applying domain-specific decay to belief: {str(e)}")
            return belief, 0.0

    def get_opinion_decay_rate(self, time_horizon: TimeHorizon) -> float:
        """
        Get the decay rate for an opinion based on its time horizon.

        Args:
            time_horizon: Time horizon of the opinion

        Returns:
            Decay rate as a float
        """
        return self.decay_rates.get(time_horizon, self.decay_rates[TimeHorizon.UNKNOWN])

    def apply_confidence_decay_to_opinion(
        self, db: Neo4jConnection, opinion: Opinion, future_time: datetime
    ) -> Tuple[Opinion, float]:
        """
        Apply temporal decay to an opinion based on its time horizon.

        Args:
            db: Neo4j connection
            opinion: Opinion to apply decay to
            future_time: Future time point

        Returns:
            Tuple of (decayed_opinion, decay_amount)
        """
        try:
            # Convert Neo4j Node to Opinion object if necessary
            if hasattr(opinion, "items"):
                opinion_data = dict(opinion.items())

                # Parse updated_at
                if "updated_at" in opinion_data:
                    try:
                        opinion_data["updated_at"] = self._convert_to_datetime(
                            opinion_data["updated_at"]
                        )
                    except ValueError:
                        logger.warning(
                            f"Could not parse updated_at: {opinion_data['updated_at']}"
                        )

                # Convert time_horizon string to enum if needed
                if "time_horizon" in opinion_data and isinstance(
                    opinion_data["time_horizon"], str
                ):
                    try:
                        opinion_data["time_horizon"] = TimeHorizon[
                            opinion_data["time_horizon"]
                        ]
                    except (KeyError, ValueError):
                        opinion_data["time_horizon"] = TimeHorizon.UNKNOWN

                # Convert stance string to enum if needed
                if "stance" in opinion_data and isinstance(opinion_data["stance"], str):
                    try:
                        opinion_data["stance"] = OpinionStance[opinion_data["stance"]]
                    except (KeyError, ValueError):
                        opinion_data["stance"] = OpinionStance.NEUTRAL

                # Parse metadata if it's a string
                if "metadata" in opinion_data and isinstance(
                    opinion_data["metadata"], str
                ):
                    try:
                        opinion_data["metadata"] = json.loads(opinion_data["metadata"])
                    except json.JSONDecodeError:
                        opinion_data["metadata"] = {}

                # Create Opinion object
                opinion = Opinion.from_dict(opinion_data)

            # Convert datetime objects
            try:
                updated_at = self._convert_to_datetime(opinion.updated_at)
                future_time = self._convert_to_datetime(future_time)
            except ValueError as e:
                logger.error(f"Error converting datetime: {str(e)}")
                return opinion, 0.0

            # Calculate days since update
            days_since_update = (future_time - updated_at).days

            # Skip if opinion was recently updated
            if days_since_update < 1:
                return opinion, 0.0

            # Get base decay rate based on time horizon
            base_decay_rate = self.get_opinion_decay_rate(opinion.time_horizon)

            # Get resistance factor with default
            resistance_factor = getattr(opinion, "resistance_factor", 0.5)

            # Apply resistance factor to decay rate
            effective_decay_rate = base_decay_rate * (1 - resistance_factor)

            # Calculate total decay (capped at 50% to prevent too much decay)
            total_decay = min(effective_decay_rate * days_since_update, 0.5)

            # Store original confidence
            original_confidence = opinion.confidence

            # Calculate new confidence (minimum confidence of 0.1)
            new_confidence = max(0.1, original_confidence * (1 - total_decay))

            # Get current metadata or initialize empty dict
            metadata = opinion.metadata or {}

            # Record decay in metadata
            metadata["temporal_decay"] = {
                "days_since_update": days_since_update,
                "total_decay": total_decay,
                "original_confidence": original_confidence,
                "decayed_confidence": new_confidence,
                "decay_rate": effective_decay_rate,
                "base_decay_rate": base_decay_rate,
                "resistance_factor": resistance_factor,
                "time_horizon": opinion.time_horizon.value,
                "decay_timestamp": datetime.now().isoformat(),
            }

            # Create new opinion with updated confidence
            decayed_opinion = Opinion(
                uid=opinion.uid,
                statement=opinion.statement,
                confidence=new_confidence,
                stance=opinion.stance,
                clarity=opinion.clarity,
                time_horizon=opinion.time_horizon,
                resistance_factor=resistance_factor,
                metadata=metadata,
                version=getattr(opinion, "version", 1) + 1,
                updated_by="temporal_decay",
                last_updated=datetime.now(),
            )

            # Save decayed opinion
            decayed_opinion.save(db)

            return decayed_opinion, total_decay

        except Exception as e:
            logger.error(f"Error applying temporal decay to opinion: {str(e)}")
            return opinion, 0.0

    def apply_decay(self, db: Neo4jConnection, days: int = 30) -> Dict[str, Any]:
        """
        Apply temporal decay to simulate the passage of time.

        Args:
            db: Neo4j connection
            days: Number of days to simulate

        Returns:
            Dictionary containing decay statistics
        """
        logger.info(f"Simulating temporal decay for {days} days")

        # Create a future time point
        future_time = datetime.now() + timedelta(days=days)

        # Get all beliefs
        belief_query = """
        MATCH (b:Belief)
        RETURN b
        """
        beliefs = db.execute_query(belief_query, {}, fetch_all=True)

        # Get all opinions
        opinion_query = """
        MATCH (o:Opinion)
        RETURN o
        """
        opinions = db.execute_query(opinion_query, {}, fetch_all=True)

        # Track statistics
        stats = {
            "total_beliefs": len(beliefs),
            "total_opinions": len(opinions),
            "beliefs_decayed": 0,
            "opinions_decayed": 0,
            "average_belief_decay": 0.0,
            "average_opinion_decay": 0.0,
        }

        # Apply decay to beliefs
        total_belief_decay = 0.0
        for belief_record in beliefs:
            belief_node = belief_record["b"]
            try:
                # Convert Neo4j Node to dict
                belief_data = dict(belief_node.items())
                belief = Belief.from_dict(belief_data)

                # Apply domain-specific decay
                decayed_belief, decay_amount = (
                    self.apply_domain_specific_decay_to_belief(db, belief, future_time)
                )

                if decay_amount > 0:
                    stats["beliefs_decayed"] += 1
                    total_belief_decay += decay_amount
            except Exception as e:
                logger.error(f"Error applying decay to belief: {str(e)}")
                continue

        # Apply decay to opinions
        total_opinion_decay = 0.0
        for opinion_record in opinions:
            opinion_node = opinion_record["o"]
            try:
                # Convert Neo4j Node to dict
                opinion_data = dict(opinion_node.items())

                # Convert time_horizon string to enum if needed
                if "time_horizon" in opinion_data and isinstance(
                    opinion_data["time_horizon"], str
                ):
                    try:
                        opinion_data["time_horizon"] = TimeHorizon(
                            opinion_data["time_horizon"]
                        )
                    except ValueError:
                        opinion_data["time_horizon"] = TimeHorizon.UNKNOWN

                # Convert stance string to enum if needed
                if "stance" in opinion_data and isinstance(opinion_data["stance"], str):
                    try:
                        opinion_data["stance"] = OpinionStance(opinion_data["stance"])
                    except ValueError:
                        opinion_data["stance"] = OpinionStance.NEUTRAL

                # Ensure metadata is properly parsed
                if "metadata" in opinion_data and isinstance(
                    opinion_data["metadata"], str
                ):
                    try:
                        opinion_data["metadata"] = json.loads(opinion_data["metadata"])
                    except json.JSONDecodeError:
                        opinion_data["metadata"] = {}

                # Create Opinion object from dictionary
                opinion = Opinion.from_dict(opinion_data)

                # Apply decay based on time horizon
                decayed_opinion, decay_amount = self.apply_confidence_decay_to_opinion(
                    db, opinion, future_time
                )

                if decay_amount > 0:
                    stats["opinions_decayed"] += 1
                    total_opinion_decay += decay_amount
            except Exception as e:
                logger.error(f"Error applying decay to opinion: {str(e)}")
                continue

        # Calculate averages
        if stats["beliefs_decayed"] > 0:
            stats["average_belief_decay"] = (
                total_belief_decay / stats["beliefs_decayed"]
            )

        if stats["opinions_decayed"] > 0:
            stats["average_opinion_decay"] = (
                total_opinion_decay / stats["opinions_decayed"]
            )

        logger.info(
            f"Applied decay to {stats['beliefs_decayed']} beliefs and {stats['opinions_decayed']} opinions"
        )
        return stats
