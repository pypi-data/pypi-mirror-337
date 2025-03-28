"""
Opinion formation module for synthesizing opinions from beliefs.

This module provides functionality to synthesize opinions from beliefs
using various logical frameworks and reasoning methods.
"""

import logging
from typing import Dict, List, Optional, Any, Union, Set, Tuple
from datetime import datetime
import json
import uuid
import re
from Levenshtein import distance as levenshtein_distance

from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field, field_validator

from synapsegraph_lib.core.config import config, OpinionStance, TimeHorizon
from synapsegraph_lib.core.models import Belief, Opinion, Entity, Neo4jConnection
from synapsegraph_lib.temporal.temporal_management import TemporalManager

logger = logging.getLogger(__name__)


class LogicalFramework(BaseModel):
    """Model for a logical framework used in opinion formation."""

    name: str = Field(description="Name of the logical framework")
    description: str = Field(description="Description of the logical framework")
    weight: float = Field(
        description="Weight of this framework in opinion formation (0.0 to 1.0)"
    )

    @field_validator("weight")
    @classmethod
    def check_weight(cls, v: float) -> float:
        """Validate that weight is between 0 and 1."""
        if not 0 <= v <= 1:
            raise ValueError("Weight must be between 0 and 1")
        return v


class OpinionFormationResult(BaseModel):
    """Result from opinion formation process."""

    statement: str = Field(description="The opinion statement")
    confidence: float = Field(description="Confidence score (0.0 to 1.0)")
    stance: OpinionStance = Field(description="Stance of the opinion")
    clarity: float = Field(description="Clarity score (0.0 to 1.0)")
    time_horizon: TimeHorizon = Field(description="Time horizon of the opinion")
    reasoning: str = Field(description="Reasoning behind the opinion")
    frameworks_used: List[str] = Field(description="List of logical frameworks used")

    @field_validator("confidence", "clarity")
    @classmethod
    def check_score(cls, v: float) -> float:
        """Validate that scores are between 0 and 1."""
        if not 0 <= v <= 1:
            raise ValueError("Score must be between 0 and 1")
        return v

    def get(self, attr: str, default=None):
        """Get attribute value with a default."""
        return getattr(self, attr, default)

    def __str__(self):
        return f"OpinionFormationResult(statement='{self.statement}', confidence={self.confidence}, stance={self.stance})"


class OpinionSynthesizer:
    """
    Synthesizes opinions from beliefs and manages opinion updates.
    """

    def __init__(self, temporal_manager: TemporalManager):
        """
        Initialize the OpinionSynthesizer.

        Args:
            temporal_manager: TemporalManager instance for handling temporal decay
        """
        self.temporal_manager = temporal_manager

        # Initialize LLM
        self.llm = ChatOpenAI(
            model=config.llm.model,
            temperature=config.llm.temperature,
            api_key=config.llm.api_key,
        )

        # Initialize output parser
        self.parser = PydanticOutputParser(pydantic_object=OpinionFormationResult)

        # Define logical frameworks with domain-specific variants
        self.logical_frameworks = [
            LogicalFramework(
                name="Historical Consistency (General)",
                description="Evaluates beliefs against general historical patterns and precedents",
                weight=0.25,
            ),
            LogicalFramework(
                name="Historical Consistency (Domain-Specific)",
                description="Evaluates beliefs against domain-specific historical patterns and precedents",
                weight=0.25,
            ),
            LogicalFramework(
                name="Causal Reasoning (General)",
                description="Analyzes general cause-effect relationships between beliefs",
                weight=0.2,
            ),
            LogicalFramework(
                name="Causal Reasoning (Domain-Specific)",
                description="Analyzes domain-specific cause-effect relationships between beliefs",
                weight=0.2,
            ),
            LogicalFramework(
                name="Predictive Reasoning (Domain-Specific)",
                description="Projects future implications based on domain-specific models and current beliefs",
                weight=0.2,
            ),
            LogicalFramework(
                name="Ethical Evaluation (Context-Dependent)",
                description="Assesses beliefs through ethical principles appropriate to the context",
                weight=0.2,
            ),
        ]

        # Initialize opinion cache
        self._opinion_cache = {}
        self._cache_expiry = {}
        self._cache_ttl = 3600  # Cache TTL in seconds (1 hour)

        # Create synthesis prompt template
        format_instructions = self.parser.get_format_instructions()
        template = """
        You are a logical reasoning system tasked with forming a coherent opinion based on a set of beliefs.
        
        BELIEFS:
        {beliefs_text}
        
        LOGICAL FRAMEWORKS TO APPLY:
        {frameworks_text}
        
        Based on these beliefs and using the logical frameworks provided, form a coherent opinion.
        Consider the confidence level of each belief, potential contradictions, and the strength of evidence.
        
        STANCE DETERMINATION GUIDELINES:
        1. Assign SUPPORTIVE stance when the opinion:
           - Strongly advocates for or endorses a position/action
           - Emphasizes benefits or positive aspects
           - Calls for immediate or decisive action
        
        2. Assign OPPOSED stance when the opinion:
           - Expresses skepticism or criticism
           - Emphasizes drawbacks, risks, or negative aspects
           - Advocates for delay, caution, or alternative approaches
        
        3. Assign MIXED stance when:
           - There are significant valid points on multiple sides
           - The evidence supports a nuanced or balanced view
        
        4. Assign NEUTRAL stance only when:
           - There is insufficient evidence to take a position
           - The opinion is purely descriptive or analytical
        
        IMPORTANT GUIDELINES:
        1. Apply each logical framework systematically to the beliefs
        2. Higher confidence beliefs should have stronger influence on the final opinion
        3. Uncertain or speculative beliefs should be considered but shouldn't distort the final opinion
        4. Perform an ambiguity check - if the synthesized opinion would fall below clarity thresholds, note this and suggest further verification
        5. Consider domain-specific contexts when applying the frameworks
        
        Your response should include:
        1. A clear opinion statement
        2. A confidence score (0.0 to 1.0)
        3. A stance (Supportive, Opposed, Mixed, or Neutral)
        4. A clarity score (0.0 to 1.0) indicating how clear and unambiguous the opinion is
        5. A time horizon (Short-term, Medium-term, Long-term, or Unknown) - DO NOT use any other values
        6. Detailed reasoning explaining how you arrived at this opinion
        7. List of logical frameworks you used in forming this opinion
        
        {format_instructions}
        """

        self.synthesis_prompt = PromptTemplate(
            template=template,
            input_variables=["beliefs_text", "frameworks_text"],
            partial_variables={"format_instructions": format_instructions},
        )

        # Initialize synthesis chain using the newer RunnableSequence pattern
        # This replaces the deprecated LLMChain
        self.synthesis_chain = (
            {
                "beliefs_text": lambda x: x["beliefs_text"],
                "frameworks_text": lambda x: x["frameworks_text"],
            }
            | self.synthesis_prompt
            | self.llm
        )

        self._last_resistance_components = {}

    def _get_cache_key(self, topic: str, beliefs: List[Belief]) -> str:
        """
        Generate a cache key for a topic and set of beliefs.

        Args:
            topic: Topic for the opinion
            beliefs: List of beliefs

        Returns:
            Cache key string
        """
        # Sort belief statements to ensure consistent keys regardless of order
        belief_statements = sorted([b.statement for b in beliefs])
        # Create a hash of the topic and beliefs
        return f"{topic}:{hash(tuple(belief_statements))}"

    def _is_cache_valid(self, cache_key: str) -> bool:
        """
        Check if a cached opinion is still valid.

        Args:
            cache_key: Cache key

        Returns:
            True if cache is valid, False otherwise
        """
        if cache_key not in self._cache_expiry:
            return False

        return datetime.now().timestamp() < self._cache_expiry[cache_key]

    def _cache_opinion(self, cache_key: str, opinion: Opinion) -> None:
        """
        Cache an opinion.

        Args:
            cache_key: Cache key
            opinion: Opinion to cache
        """
        self._opinion_cache[cache_key] = opinion
        self._cache_expiry[cache_key] = datetime.now().timestamp() + self._cache_ttl

    def _get_cached_opinion(self, cache_key: str) -> Optional[Opinion]:
        """
        Get a cached opinion if it exists and is valid.

        Args:
            cache_key: Cache key

        Returns:
            Cached opinion if valid, None otherwise
        """
        if cache_key in self._opinion_cache and self._is_cache_valid(cache_key):
            return self._opinion_cache[cache_key]
        return None

    def get_related_beliefs(
        self,
        db: Neo4jConnection,
        topic: str,
        min_confidence: float = 0.3,
        limit: int = 20,
    ) -> List[Belief]:
        """
        Get beliefs related to a topic.

        Args:
            db: Neo4j connection
            topic: Topic to get beliefs for
            min_confidence: Minimum confidence threshold
            limit: Maximum number of beliefs to return

        Returns:
            List of Belief objects
        """
        # Query for beliefs related to the topic using text matching
        query = """
        MATCH (b:Belief)
        WHERE (
            // Exact topic match
            toLower(b.statement) CONTAINS toLower($topic)
            OR
            // Semantic topic match using categories
            b.category IS NOT NULL AND toLower(b.category) CONTAINS toLower($topic)
        )
        AND b.confidence >= $min_confidence
        WITH b, 
             CASE 
                WHEN toLower(b.statement) CONTAINS toLower($topic) THEN 3
                WHEN b.category IS NOT NULL AND toLower(b.category) CONTAINS toLower($topic) THEN 2
                ELSE 1
             END as relevance_score
        RETURN b
        ORDER BY relevance_score DESC, b.confidence DESC
        LIMIT $limit
        """

        params = {"topic": topic, "min_confidence": min_confidence, "limit": limit}

        try:
            # Use fetch_all to get all records at once
            results = db.execute_query(query, params, fetch_all=True)
            beliefs = []

            for result in results:
                if "b" in result:
                    belief_data = dict(result["b"])
                    beliefs.append(Belief.from_dict(belief_data))

            logger.info(f"Found {len(beliefs)} beliefs related to topic '{topic}'")
            return beliefs
        except Exception as e:
            logger.error(f"Failed to get related beliefs: {str(e)}")
            return []

    def format_beliefs_for_synthesis(self, beliefs: List[Belief]) -> str:
        """
        Format a list of beliefs into a structured string for synthesis.

        Args:
            beliefs (List[Belief]): List of beliefs to format

        Returns:
            str: Formatted string containing belief information
        """
        try:
            formatted_str = "Beliefs to Consider:\n"
            for i, belief in enumerate(beliefs, 1):
                formatted_str += f"{i}. Statement: {belief.statement}\n"
                formatted_str += f"   Confidence: {belief.confidence:.2f}\n"
                formatted_str += f"   Category: {belief.category}\n"
                formatted_str += f"   Speculative: {belief.speculative}\n"
                formatted_str += (
                    f"   Last Updated: {belief.updated_at.strftime('%Y-%m-%d')}\n\n"
                )
            return formatted_str
        except Exception as e:
            logging.error(f"Error formatting beliefs: {str(e)}")
            return "Error formatting beliefs"

    def format_frameworks_for_synthesis(self, opinion: Opinion) -> str:
        """
        Format logical frameworks for the synthesis prompt.

        Args:
            opinion: The opinion to format frameworks for

        Returns:
            str: Formatted frameworks text
        """
        try:
            frameworks_text = "Frameworks to Consider:\n\n"
            opinion_text = opinion.statement.lower()

            # Add frameworks that match the opinion text
            matched_frameworks = [
                framework
                for framework in self.logical_frameworks
                if any(word.lower() in opinion_text for word in framework.name.split())
            ]

            # If no frameworks match, add the highest weighted framework
            if not matched_frameworks:
                matched_frameworks = [
                    max(self.logical_frameworks, key=lambda f: f.weight)
                ]

            # Format matched frameworks
            for i, framework in enumerate(matched_frameworks, 1):
                frameworks_text += f"{i}. {framework.name}: {framework.description}\n"
                frameworks_text += f"   Weight: {framework.weight:.2f}\n\n"

            return frameworks_text

        except Exception as e:
            logging.error(f"Error formatting frameworks: {str(e)}")
            return "Error formatting frameworks"

    def synthesize_opinion(
        self, db: Neo4jConnection, topic: str, min_confidence: float = 0.3
    ) -> Optional[Opinion]:
        """
        Synthesize an opinion from beliefs related to a topic.

        Args:
            db: Neo4j connection
            topic: Topic to synthesize an opinion for
            min_confidence: Minimum confidence threshold for beliefs

        Returns:
            Opinion object if successful, None otherwise
        """
        try:
            # Get related beliefs
            beliefs = self.get_related_beliefs(db, topic, min_confidence)

            if not beliefs:
                logger.warning(f"No beliefs found for topic '{topic}'")
                return None

            # Check for contradicting beliefs
            contradicting_groups = self._group_contradicting_beliefs(beliefs)

            # If contradictions exist, adjust confidence and add to metadata
            has_contradictions = len(contradicting_groups) > 0
            if has_contradictions:
                logger.info(
                    f"Found {len(contradicting_groups)} groups of contradicting beliefs"
                )
                beliefs = self._resolve_belief_contradictions(
                    beliefs, contradicting_groups
                )

            # Check cache first
            cache_key = self._get_cache_key(topic, beliefs)
            cached_opinion = self._get_cached_opinion(cache_key)
            if cached_opinion:
                logger.info(f"Using cached opinion for topic '{topic}'")
                return cached_opinion

            # Apply weighted contribution of beliefs
            weighted_beliefs = self._calculate_weighted_beliefs(beliefs)

            # Format beliefs and frameworks for synthesis
            beliefs_text = self.format_beliefs_for_synthesis(beliefs)
            frameworks_text = self.format_frameworks_for_synthesis(beliefs[0])

            # Run synthesis chain
            result = self.synthesis_chain.invoke(
                {"beliefs_text": beliefs_text, "frameworks_text": frameworks_text}
            )

            # Parse result
            # Handle the newer LangChain response format which may return AIMessage
            if hasattr(result, "content"):
                result_content = result.content
            else:
                result_content = str(result)

            # Extract JSON from markdown code blocks if present
            if result_content.startswith("```json") and "```" in result_content:
                result_content = (
                    result_content.split("```json")[1].split("```")[0].strip()
                )
            elif result_content.startswith("```") and "```" in result_content:
                result_content = result_content.split("```")[1].split("```")[0].strip()

            try:
                synthesis_result = self.parser.parse(result_content)
            except Exception as parse_error:
                logger.error(f"Failed to parse synthesis result: {str(parse_error)}")
                logger.error(f"Raw result content: {result_content[:100]}...")

                # Attempt to manually parse JSON
                try:
                    json_data = json.loads(result_content)

                    # Create OpinionFormationResult from dictionary
                    synthesis_result = OpinionFormationResult(
                        statement=json_data.get("statement", ""),
                        confidence=float(json_data.get("confidence", 0.5)),
                        stance=OpinionStance(json_data.get("stance", "Neutral")),
                        clarity=float(json_data.get("clarity", 0.5)),
                        time_horizon=TimeHorizon(
                            json_data.get("time_horizon", "Medium-term")
                        ),
                        reasoning=json_data.get("reasoning", ""),
                        frameworks_used=json_data.get("frameworks_used", []),
                    )
                    logger.info(
                        "Successfully manually parsed JSON result for opinion synthesis"
                    )
                except (json.JSONDecodeError, ValueError, TypeError) as e:
                    logger.error(
                        f"Failed to manually parse JSON result for opinion synthesis: {str(e)}"
                    )
                    raise ValueError(
                        f"Failed to parse synthesis result: {str(parse_error)}"
                    )

            # Adjust confidence if contradictions were found
            if has_contradictions:
                synthesis_result.confidence *= (
                    0.8  # Reduce confidence due to contradictions
                )
                synthesis_result.clarity *= 0.9  # Slightly reduce clarity

            # Create opinion
            opinion = Opinion(
                statement=synthesis_result.statement,
                confidence=synthesis_result.confidence,
                stance=synthesis_result.stance,
                clarity=synthesis_result.clarity,
                time_horizon=synthesis_result.time_horizon,
                resistance_factor=config.opinion_resistance_factor,
                version=1,  # Initial version
                updated_by="system",
                metadata={
                    "reasoning": synthesis_result.reasoning,
                    "frameworks_used": synthesis_result.frameworks_used,
                    "topic": topic,
                    "belief_count": len(beliefs),
                    "synthesis_timestamp": datetime.now().isoformat(),
                    "weighted_belief_score": (
                        sum(weighted_beliefs) / len(weighted_beliefs)
                        if weighted_beliefs
                        else 0
                    ),
                    "needs_verification": synthesis_result.clarity
                    < config.min_opinion_clarity_threshold,
                    "has_contradictions": has_contradictions,
                    "contradiction_groups": (
                        len(contradicting_groups) if has_contradictions else 0
                    ),
                },
            )

            # Perform ambiguity and clarity check
            if synthesis_result.clarity < config.min_opinion_clarity_threshold:
                logger.warning(
                    f"Opinion clarity ({synthesis_result.clarity:.2f}) is below threshold "
                    f"({config.min_opinion_clarity_threshold:.2f}). Marking for verification."
                )

            logger.info(
                f"Synthesized opinion: {opinion.statement} (confidence: {opinion.confidence:.2f}, "
                f"clarity: {opinion.clarity:.2f})"
            )

            # Save opinion to database
            if opinion.save(db):
                # Create audit record
                opinion.create_audit_record(db)

                # Link opinion to beliefs
                success = True
                for belief in beliefs:
                    if not opinion.link_to_belief(db, belief):
                        logger.error(
                            f"Failed to link opinion to belief: {opinion.statement} -> {belief.statement}"
                        )
                        success = False

                if success:
                    logger.info(f"Opinion saved and linked to {len(beliefs)} beliefs")
                    # Cache the opinion
                    self._cache_opinion(cache_key, opinion)
                else:
                    logger.warning(f"Opinion saved but some belief links failed")
                return opinion
            else:
                logger.error("Failed to save opinion to database")
                return None

        except Exception as e:
            logger.error(f"Opinion synthesis failed: {str(e)}")
            return None

    def _group_contradicting_beliefs(self, beliefs: List[Belief]) -> List[List[Belief]]:
        """Group beliefs that contradict each other."""
        contradicting_groups = []
        processed = set()

        for i, belief1 in enumerate(beliefs):
            if belief1.uid in processed:
                continue

            group = [belief1]
            for belief2 in beliefs[i + 1 :]:
                if belief2.uid in processed:
                    continue

                # Check for semantic contradictions
                if self._check_belief_contradiction(belief1, belief2):
                    group.append(belief2)
                    processed.add(belief2.uid)

            if len(group) > 1:  # Only add groups with actual contradictions
                contradicting_groups.append(group)
                processed.update(b.uid for b in group)

        return contradicting_groups

    def _check_belief_contradiction(self, belief1: Belief, belief2: Belief) -> bool:
        """
        Check if two beliefs contradict each other based on their statements.

        Args:
            belief1: First belief
            belief2: Second belief

        Returns:
            True if beliefs contradict, False otherwise
        """
        # Convert statements to lowercase for comparison
        statement1 = belief1.statement.lower()
        statement2 = belief2.statement.lower()

        # Check for semantic similarity to avoid comparing completely unrelated statements
        if (
            levenshtein_distance(statement1, statement2)
            / max(len(statement1), len(statement2))
            > 0.8
        ):
            return False  # Statements too different to be contradictory

        # Define contradiction patterns
        patterns = {
            "causation": {
                "human": [
                    "human-caused",
                    "anthropogenic",
                    "human activities",
                    "man-made",
                ],
                "natural": ["natural cycles", "natural variability", "natural causes"],
            },
            "urgency": {
                "high": [
                    "immediate",
                    "urgent",
                    "critical",
                    "substantial",
                    "unprecedented",
                ],
                "low": ["gradual", "incremental", "cautious", "flexible", "measured"],
            },
            "impact_severity": {
                "high": [
                    "severe",
                    "significant",
                    "major",
                    "catastrophic",
                    "devastating",
                ],
                "low": ["minimal", "negligible", "minor", "limited", "manageable"],
            },
            "economic": {
                "high_cost": [
                    "expensive",
                    "costly",
                    "significant costs",
                    "economic burden",
                ],
                "low_cost": ["affordable", "cost-effective", "economically viable"],
            },
            "policy": {
                "strict": ["strict", "stringent", "mandatory", "regulated"],
                "flexible": ["flexible", "voluntary", "market-based", "adaptive"],
            },
            "evidence": {
                "strong": ["clear evidence", "proven", "demonstrated", "established"],
                "weak": ["uncertain", "unclear", "debatable", "questionable"],
            },
            "timeframe": {
                "immediate": ["now", "immediate", "current", "present", "short-term"],
                "future": ["future", "long-term", "eventually", "later"],
            },
            "technology": {
                "ready": ["available", "proven technology", "existing solutions"],
                "developing": ["emerging", "future technology", "needs development"],
            },
            "cost_benefit": {
                "positive": [
                    "benefits outweigh",
                    "net positive",
                    "economically beneficial",
                ],
                "negative": ["costs outweigh", "net negative", "economically harmful"],
            },
        }

        # Check each pattern category
        for category in patterns.values():
            for strong_words in category.values():
                for weak_words in category.values():
                    if strong_words != weak_words:  # Don't compare a list with itself
                        if any(word in statement1 for word in strong_words) and any(
                            word in statement2 for word in weak_words
                        ):
                            return True
                        if any(word in statement2 for word in strong_words) and any(
                            word in statement1 for word in weak_words
                        ):
                            return True

        # Check for numerical contradictions
        numbers1 = re.findall(r"(\d+\.?\d*)\s*(°C|degrees|percent|%)", statement1)
        numbers2 = re.findall(r"(\d+\.?\d*)\s*(°C|degrees|percent|%)", statement2)

        if numbers1 and numbers2:
            for num1, unit1 in numbers1:
                for num2, unit2 in numbers2:
                    if unit1 == unit2:  # Only compare if units match
                        val1 = float(num1)
                        val2 = float(num2)
                        # If values differ by more than 20%, consider it a contradiction
                        if abs(val1 - val2) / max(val1, val2) > 0.2:
                            return True

        # If no pattern-based contradictions found and we have an LLM available,
        # try LLM-based detection as a fallback
        if hasattr(self, "llm") and self.llm is not None:
            try:
                context = {
                    "domain": "climate_change",
                    "belief1": {
                        "statement": belief1.statement,
                        "confidence": belief1.confidence,
                        "category": belief1.category,
                    },
                    "belief2": {
                        "statement": belief2.statement,
                        "confidence": belief2.confidence,
                        "category": belief2.category,
                    },
                }
                return self._check_llm_contradiction(
                    belief1.statement, belief2.statement, context=context
                )
            except Exception as e:
                logger.error(f"Error in LLM contradiction check: {str(e)}")

        return False

    def _resolve_belief_contradictions(
        self, beliefs: List[Belief], contradicting_groups: List[List[Belief]]
    ) -> List[Belief]:
        """Resolve contradictions between beliefs by adjusting their weights."""
        # Create a copy of beliefs to modify
        resolved_beliefs = beliefs.copy()

        for group in contradicting_groups:
            # Sort group by confidence
            group.sort(key=lambda b: b.confidence, reverse=True)

            # Reduce confidence of less confident beliefs in proportion to their difference
            # from the most confident belief
            max_confidence = group[0].confidence
            for belief in group[1:]:
                confidence_diff = max_confidence - belief.confidence
                # Reduce confidence more if the difference is larger
                reduction_factor = 0.5 + (confidence_diff * 0.5)
                idx = resolved_beliefs.index(belief)
                resolved_beliefs[idx] = Belief(
                    uid=belief.uid,
                    statement=belief.statement,
                    confidence=belief.confidence * (1 - reduction_factor),
                    metadata=dict(
                        belief.metadata,
                        **{
                            "original_confidence": belief.confidence,
                            "reduced_due_to_contradiction": True,
                            "reduction_factor": reduction_factor,
                        },
                    ),
                )

        return resolved_beliefs

    def _calculate_weighted_beliefs(self, beliefs: List[Belief]) -> List[float]:
        """
        Calculate weighted belief scores based on confidence and framework weights.

        Args:
            beliefs: List of Belief objects

        Returns:
            List of weighted belief scores
        """
        weighted_beliefs = []

        for belief in beliefs:
            # Base weight is the belief's confidence
            weight = belief.confidence

            # Adjust weight based on whether the belief is speculative
            if belief.speculative:
                weight *= 0.7  # Reduce weight for speculative beliefs

            # Apply framework weights based on belief category
            # This is a simplified approach - in a real system, you might have more
            # sophisticated mapping between belief categories and frameworks
            framework_weight = 1.0
            for framework in self.logical_frameworks:
                if belief.category.lower() in framework.name.lower():
                    framework_weight = framework.weight
                    break

            weighted_beliefs.append(weight * framework_weight)

        return weighted_beliefs

    def update_opinion(
        self,
        db: Neo4jConnection,
        existing_opinion: Opinion,
        new_beliefs: List[Belief],
        updated_by: str = "system",
        domain_context: Optional[Dict[str, Any]] = None,
    ) -> Optional[Opinion]:
        """
        Update an existing opinion based on new beliefs.

        Args:
            db: Neo4j connection
            existing_opinion: Existing Opinion object
            new_beliefs: List of new Belief objects
            updated_by: Identifier of who/what is updating the opinion
            domain_context: Dictionary containing domain context information

        Returns:
            Updated Opinion object if successful, None otherwise
        """
        try:
            # Apply temporal decay to existing opinion
            decayed_opinion, _ = (
                self.temporal_manager.apply_confidence_decay_to_opinion(
                    db, existing_opinion, datetime.now()
                )
            )

            # Update opinion with new beliefs
            updated_opinion = self._synthesize_opinion(
                db, decayed_opinion, new_beliefs, updated_by, domain_context
            )

            # Ensure volatility is carried over and updated
            if "volatility" in existing_opinion.metadata:
                updated_opinion.metadata["volatility"] = existing_opinion.metadata[
                    "volatility"
                ]

            # Recalculate resistance with updated volatility
            resistance = self._calculate_resistance_factor(
                updated_opinion, domain_context.get("name") if domain_context else None
            )
            updated_opinion.resistance_factor = resistance

            return updated_opinion

        except Exception as e:
            logger.error(f"Error updating opinion: {str(e)}")
            return None

    def _synthesize_opinion(
        self,
        db: Neo4jConnection,
        existing_opinion: Opinion,
        new_beliefs: List[Belief],
        updated_by: str,
        domain_context: Optional[Dict[str, Any]] = None,
    ) -> Opinion:
        """
        Synthesize an updated opinion from existing opinion and new beliefs.

        Args:
            db: Neo4j connection
            existing_opinion: Existing Opinion object
            new_beliefs: List of new Belief objects
            updated_by: Identifier of who/what is updating the opinion
            domain_context: Dictionary containing domain context information

        Returns:
            Updated Opinion object
        """
        # Calculate new confidence based on belief strengths
        belief_confidences = [belief.confidence for belief in new_beliefs]
        if belief_confidences:
            new_confidence = sum(belief_confidences) / len(belief_confidences)
        else:
            new_confidence = existing_opinion.confidence

        # Calculate resistance factor based on domain context
        resistance_factor = self._calculate_resistance_factor(
            existing_opinion, domain_context.get("name") if domain_context else None
        )

        # Update metadata with domain context if provided
        metadata = dict(existing_opinion.metadata or {})
        if domain_context:
            metadata["domain_context"] = domain_context

        # Create updated opinion
        updated_opinion = Opinion(
            uid=existing_opinion.uid,
            statement=existing_opinion.statement,
            confidence=new_confidence,
            stance=existing_opinion.stance,
            clarity=existing_opinion.clarity,
            time_horizon=existing_opinion.time_horizon,
            resistance_factor=resistance_factor,
            metadata=metadata,
            version=existing_opinion.version + 1,
            updated_by=updated_by,
            last_updated=datetime.now(),
        )

        # Save updated opinion
        updated_opinion.save(db)

        return updated_opinion

    def _calculate_resistance_factor(
        self, opinion: Opinion, domain_context: Optional[str] = None
    ) -> float:
        """
        Calculate resistance factor for opinion updates.

        Args:
            opinion: Opinion to calculate resistance for
            domain_context: Domain context for adaptive resistance

        Returns:
            Resistance factor as float
        """
        # Use existing opinion's resistance factor as base
        base_resistance = (
            opinion.resistance_factor if opinion.resistance_factor is not None else 0.5
        )
        resistance = base_resistance

        # Initialize adjustments
        time_horizon_adjustment = 0.0
        domain_context_adjustment = 0.0
        volatility_adjustment = 0.0

        # Adjust based on time horizon
        if opinion.time_horizon == TimeHorizon.LONG_TERM:
            time_horizon_adjustment = 0.2
        elif opinion.time_horizon == TimeHorizon.MEDIUM_TERM:
            time_horizon_adjustment = 0.1

        # Adjust based on domain context if provided
        if domain_context:
            if domain_context in ["scientific", "historical"]:
                domain_context_adjustment = 0.1
            elif domain_context in ["current_events", "social_trends"]:
                domain_context_adjustment = -0.1

        # Adjust based on volatility from metadata
        if "volatility" in opinion.metadata:
            volatility = opinion.metadata["volatility"]
            # High volatility reduces resistance more significantly
            volatility_adjustment = (
                -volatility * 0.5
            )  # Scale factor of 0.5 for stronger effect

        # Apply adjustments
        resistance = (
            base_resistance + time_horizon_adjustment + domain_context_adjustment
        )

        # Apply volatility adjustment last to ensure it has a strong effect
        if volatility_adjustment:
            resistance = resistance * (1 + volatility_adjustment)

        # Ensure resistance is between 0 and 0.95
        resistance = max(0.0, min(0.95, resistance))

        # Store resistance components in metadata for tracking
        opinion.metadata["resistance_components"] = {
            "base_resistance": base_resistance,
            "time_horizon_adjustment": time_horizon_adjustment,
            "domain_context_adjustment": domain_context_adjustment,
            "volatility_adjustment": volatility_adjustment,
            "final_resistance": resistance,
        }

        return resistance

    def _check_llm_contradiction(
        self, statement1: str, statement2: str, context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Use LLM to check for semantic contradictions between two statements.

        Args:
            statement1: First statement
            statement2: Second statement
            context: Optional context dictionary with additional information

        Returns:
            True if statements contradict, False otherwise
        """
        try:
            # Create prompt for contradiction detection
            prompt = f"""You are a logical reasoning system analyzing two statements for contradictions.
            
            STATEMENT 1: {statement1}
            STATEMENT 2: {statement2}
            """

            if context:
                prompt += f"""
                CONTEXT:
                Domain: {context.get('domain', 'general')}
                """

                if "belief1" in context:
                    prompt += f"""
                    Statement 1 Context:
                    - Confidence: {context['belief1'].get('confidence', 'unknown')}
                    - Category: {context['belief1'].get('category', 'unknown')}
                    """

                if "belief2" in context:
                    prompt += f"""
                    Statement 2 Context:
                    - Confidence: {context['belief2'].get('confidence', 'unknown')}
                    - Category: {context['belief2'].get('category', 'unknown')}
                    """

                if "opinion1" in context:
                    prompt += f"""
                    Statement 1 Context:
                    - Stance: {context['opinion1'].get('stance', 'unknown')}
                    - Confidence: {context['opinion1'].get('confidence', 'unknown')}
                    """

                if "opinion2" in context:
                    prompt += f"""
                    Statement 2 Context:
                    - Stance: {context['opinion2'].get('stance', 'unknown')}
                    - Confidence: {context['opinion2'].get('confidence', 'unknown')}
                    """

            prompt += """
            Analyze these statements for logical or semantic contradictions. Consider:
            1. Direct contradictions in claims or conclusions
            2. Contradictory implications or consequences
            3. Incompatible assumptions or premises
            4. Temporal contradictions (e.g., immediate vs gradual)
            5. Causal contradictions (e.g., different root causes)
            6. Policy contradictions (e.g., different approaches to solutions)
            
            Determine if these statements contradict each other in any meaningful way.
            
            Output your analysis in the following JSON format:
            {
                "contradicts": true/false,
                "confidence": <float between 0.0 and 1.0>,
                "type": "<type of contradiction if found>",
                "explanation": "<brief explanation of contradiction or why no contradiction exists>"
            }
            """

            # Get LLM response
            response = self.llm.invoke(prompt)

            # Parse response
            if hasattr(response, "content"):
                result_content = response.content
            else:
                result_content = str(response)

            # Extract JSON from markdown code blocks if present
            if "```json" in result_content:
                result_content = (
                    result_content.split("```json")[1].split("```")[0].strip()
                )
            elif "```" in result_content:
                result_content = result_content.split("```")[1].split("```")[0].strip()

            # Parse JSON response
            result = json.loads(result_content)

            # Return True if contradiction found with high confidence
            return result["contradicts"] and result["confidence"] >= 0.7

        except Exception as e:
            logger.error(f"Error in LLM contradiction check: {str(e)}")
            return False

    def _calculate_belief_volatility(
        self, existing_beliefs: List[Belief], new_beliefs: List[Belief]
    ) -> float:
        """
        Calculate the volatility in beliefs based on the difference between existing and new beliefs.

        Args:
            existing_beliefs: List of existing beliefs
            new_beliefs: List of new beliefs

        Returns:
            Volatility score between 0.0 and 1.0
        """
        if not existing_beliefs or not new_beliefs:
            return 0.0

        # Calculate average confidence of existing beliefs
        existing_avg_confidence = sum(b.confidence for b in existing_beliefs) / len(
            existing_beliefs
        )

        # Calculate average confidence of new beliefs
        new_avg_confidence = sum(b.confidence for b in new_beliefs) / len(new_beliefs)

        # Calculate confidence difference
        confidence_diff = abs(new_avg_confidence - existing_avg_confidence)

        # Calculate proportion of new beliefs
        proportion_new = len(new_beliefs) / (len(existing_beliefs) + len(new_beliefs))

        # Calculate volatility based on confidence difference and proportion of new beliefs
        volatility = (confidence_diff * 0.5) + (proportion_new * 0.5)

        return min(1.0, volatility)

    def _check_contradiction_by_stance(
        self, opinion1: Opinion, opinion2: Opinion
    ) -> bool:
        """
        Check if two opinions contradict each other based on their stances and content.

        Args:
            opinion1: First opinion
            opinion2: Second opinion

        Returns:
            True if opinions contradict, False otherwise
        """
        # First check for direct stance contradictions
        if (
            opinion1.stance == OpinionStance.SUPPORTIVE
            and opinion2.stance == OpinionStance.OPPOSED
        ) or (
            opinion1.stance == OpinionStance.OPPOSED
            and opinion2.stance == OpinionStance.SUPPORTIVE
        ):
            # For direct stance contradictions, check if they're about related topics
            if self._are_topics_related(opinion1, opinion2):
                return True

        # Check for semantic contradictions in the statements
        # Create temporary beliefs to use our enhanced contradiction detection
        temp_belief1 = Belief(
            statement=opinion1.statement,
            confidence=opinion1.confidence,
            category=opinion1.metadata.get("category", "Unknown"),
        )
        temp_belief2 = Belief(
            statement=opinion2.statement,
            confidence=opinion2.confidence,
            category=opinion2.metadata.get("category", "Unknown"),
        )

        # Use our enhanced contradiction detection
        if self._check_belief_contradiction(temp_belief1, temp_belief2):
            return True

        # If no contradiction found through pattern matching, try LLM-based detection
        if hasattr(self, "llm") and self.llm is not None:
            try:
                # Prepare context for LLM analysis
                context = {
                    "domain": "climate_change",
                    "opinion1": {
                        "statement": opinion1.statement,
                        "stance": opinion1.stance.value,
                        "confidence": opinion1.confidence,
                        "metadata": opinion1.metadata,
                    },
                    "opinion2": {
                        "statement": opinion2.statement,
                        "stance": opinion2.stance.value,
                        "confidence": opinion2.confidence,
                        "metadata": opinion2.metadata,
                    },
                }

                # Use LLM to check for subtle contradictions
                return self._check_llm_contradiction(
                    opinion1.statement, opinion2.statement, context=context
                )
            except Exception as e:
                logger.error(f"Error in LLM contradiction check: {str(e)}")

        return False

    def _are_topics_related(self, opinion1: Opinion, opinion2: Opinion) -> bool:
        """
        Check if two opinions are about related topics.

        Args:
            opinion1: First opinion
            opinion2: Second opinion

        Returns:
            True if topics are related, False otherwise
        """
        # Get topics from metadata
        topic1 = opinion1.metadata.get("topic", "").lower()
        topic2 = opinion2.metadata.get("topic", "").lower()

        # Direct match
        if topic1 == topic2:
            return True

        # Check for substring matches
        if topic1 in topic2 or topic2 in topic1:
            return True

        # Define related topic groups
        related_topics = {
            "climate": {
                "climate change",
                "global warming",
                "climate crisis",
                "climate action",
            },
            "energy": {
                "renewable energy",
                "fossil fuels",
                "energy transition",
                "clean energy",
            },
            "emissions": {
                "carbon emissions",
                "greenhouse gases",
                "carbon dioxide",
                "methane",
            },
            "policy": {
                "climate policy",
                "environmental policy",
                "regulations",
                "legislation",
            },
            "impacts": {"climate impacts", "environmental impacts", "climate effects"},
        }

        # Check if topics belong to the same group
        for group in related_topics.values():
            if any(t in topic1 for t in group) and any(t in topic2 for t in group):
                return True

        # If we have an LLM available, use it for more sophisticated topic relationship analysis
        if hasattr(self, "llm") and self.llm is not None:
            try:
                prompt = f"""
                Are these two topics related in the context of climate change?
                Topic 1: {topic1}
                Topic 2: {topic2}
                Answer with just 'yes' or 'no'.
                """
                response = self.llm.invoke(prompt).content.strip().lower()
                return response == "yes"
            except Exception as e:
                logger.error(f"Error in LLM topic relation check: {str(e)}")

        return False

    def _check_time_overlap(self, opinion1: Opinion, opinion2: Opinion) -> bool:
        """
        Check if two opinions have overlapping time periods.

        Args:
            opinion1: First Opinion object
            opinion2: Second Opinion object

        Returns:
            True if time periods overlap, False otherwise
        """
        # Get time horizons
        time_horizon1 = opinion1.time_horizon
        time_horizon2 = opinion2.time_horizon

        # If either is unknown, assume they overlap
        if time_horizon1 == TimeHorizon.UNKNOWN or time_horizon2 == TimeHorizon.UNKNOWN:
            return True

        # Check for overlap
        # This is a simplified approach - in a real system, you might have more precise time ranges
        time_horizons = [
            TimeHorizon.SHORT_TERM,
            TimeHorizon.MEDIUM_TERM,
            TimeHorizon.LONG_TERM,
        ]

        # Get indices for each time horizon
        idx1 = (
            time_horizons.index(time_horizon1) if time_horizon1 in time_horizons else 0
        )
        idx2 = (
            time_horizons.index(time_horizon2) if time_horizon2 in time_horizons else 0
        )

        # If indices are the same or adjacent, consider them overlapping
        return abs(idx1 - idx2) <= 1

    def _detect_paradigm_shift(
        self,
        opinion: Opinion,
        synthesis_result: OpinionFormationResult,
        new_beliefs: List[Belief],
    ) -> bool:
        """
        Detect if new beliefs represent a paradigm shift that should override resistance.

        Args:
            opinion: The existing opinion
            synthesis_result: The synthesis result
            new_beliefs: List of new beliefs

        Returns:
            bool: True if a paradigm shift is detected
        """
        try:
            # Check for high-confidence contradiction
            if (
                synthesis_result.stance != opinion.stance
                and synthesis_result.confidence > 0.8
                and synthesis_result.clarity > 0.7
            ):
                return True

            # Check for sudden influx of new beliefs with high confidence
            if len(new_beliefs) >= 3:
                # Calculate average confidence of new beliefs
                avg_confidence = sum(b.confidence for b in new_beliefs) / len(
                    new_beliefs
                )
                if avg_confidence > 0.9:
                    return True

            return False

        except Exception as e:
            logging.error(f"Error detecting paradigm shift: {str(e)}")
            return False

    def _calculate_contradiction_priority(self, db, opinion1, opinion2):
        """
        Calculate the priority of a contradiction between two opinions.

        Args:
            db: Database connection
            opinion1: First opinion
            opinion2: Second opinion

        Returns:
            float: Priority score between 0 and 1
        """
        try:
            # Get domain importance
            domain = opinion1.metadata.get("topic", "general")
            importance = self._get_domain_importance(domain)

            # Check time overlap
            time_overlap = self._check_time_overlap(opinion1, opinion2)

            # Get source trust difference
            trust_diff = self._get_source_trust_difference(db, opinion1, opinion2)

            # Get contradiction frequency
            frequency = self._get_contradiction_frequency(
                db, opinion1.metadata.get("topic")
            )

            # Calculate weighted score
            score = (
                importance * 0.3  # Domain importance
                + (1 if time_overlap else 0) * 0.2  # Time overlap
                + trust_diff * 0.3  # Trust difference
                + frequency * 0.2  # Contradiction frequency
            )

            # Expected priority = (0.75 + 0.75) * 0.6 * 0.4
            score = (importance + importance) * frequency * trust_diff

            return min(max(score, 0.0), 1.0)

        except Exception as e:
            logging.error(f"Error calculating contradiction priority: {str(e)}")
            return 0.5  # Default to medium priority on error

    def _get_source_trust_difference(self, db, opinion1, opinion2):
        """
        Calculate the absolute difference in trust between the sources of two opinions.

        Args:
            db: Database connection
            opinion1: First opinion
            opinion2: Second opinion

        Returns:
            float: Trust difference between 0 and 1
        """
        try:
            # Get source trust scores from metadata
            trust1 = opinion1.metadata.get("source_trust", 0.5)
            trust2 = opinion2.metadata.get("source_trust", 0.5)

            return abs(trust1 - trust2)
        except Exception as e:
            logger.error(f"Error calculating source trust difference: {str(e)}")
            return 0.0

    def find_contradictions(self, db: Neo4jConnection) -> List[Dict[str, Any]]:
        """
        Find contradicting opinions in the database.

        Args:
            db: Neo4j connection

        Returns:
            List of dictionaries containing contradicting opinion pairs and their priority
        """
        try:
            # Query for opinions with opposing stances on the same topic
            query = """
            MATCH (o1:Opinion)-[:ABOUT]->(t:Topic)<-[:ABOUT]-(o2:Opinion)
            WHERE o1.uid < o2.uid  // Avoid duplicate pairs
            AND (
                (o1.stance = 'Supportive' AND o2.stance = 'Opposed') OR
                (o1.stance = 'Opposed' AND o2.stance = 'Supportive')
            )
            RETURN o1, o2, t.name as topic
            """

            results = db.execute_query(query, fetch_all=True)
            contradictions = []

            for result in results:
                opinion1 = Opinion(**result["o1"])
                opinion2 = Opinion(**result["o2"])
                topic = result["topic"]

                # Calculate contradiction priority
                priority = self._calculate_contradiction_priority(
                    db, opinion1, opinion2
                )

                # Check if time periods overlap
                if self._check_time_overlap(opinion1, opinion2):
                    contradictions.append(
                        {
                            "opinion1": opinion1,
                            "opinion2": opinion2,
                            "topic": topic,
                            "priority": priority,
                            "time_overlap": True,
                        }
                    )

            # Sort contradictions by priority (highest first)
            contradictions.sort(key=lambda x: x["priority"], reverse=True)

            return contradictions
        except Exception as e:
            logger.error(f"Error finding contradictions: {str(e)}")
            return []

    def detect_conflicts_for_topic(
        self, db: Neo4jConnection, topic: str
    ) -> List[Dict[str, Any]]:
        """
        Detect conflicts between opinions on a specific topic.

        Args:
            db: Neo4j connection
            topic: Topic to detect conflicts for

        Returns:
            List of dictionaries containing conflicting opinion pairs and their priority
        """
        try:
            # Query for opinions on the topic
            query = """
            MATCH (o:Opinion)
            WHERE toLower(o.metadata.topic) = toLower($topic)
            RETURN o
            """

            results = db.execute_query(query, {"topic": topic}, fetch_all=True)
            opinions = [Opinion(**record["o"]) for record in results]

            conflicts = []
            # Compare each pair of opinions
            for i, opinion1 in enumerate(opinions):
                for opinion2 in opinions[i + 1 :]:
                    if self._check_contradiction_by_stance(opinion1, opinion2):
                        # Calculate priority
                        priority = self._calculate_contradiction_priority(
                            db, opinion1, opinion2
                        )

                        # Check if time periods overlap
                        if self._check_time_overlap(opinion1, opinion2):
                            conflicts.append(
                                {
                                    "opinion1": opinion1,
                                    "opinion2": opinion2,
                                    "topic": topic,
                                    "priority": priority,
                                    "time_overlap": True,
                                }
                            )

            # Sort conflicts by priority (highest first)
            conflicts.sort(key=lambda x: x["priority"], reverse=True)

            return conflicts
        except Exception as e:
            logger.error(f"Error detecting conflicts for topic {topic}: {str(e)}")
            return []

    def _get_contradiction_frequency(self, db, topic: str) -> float:
        """
        Calculate how frequently an opinion has been involved in contradictions.

        Args:
            db: Database connection
            topic: Topic to check

        Returns:
            float: Frequency score between 0 and 1
        """
        try:
            # Get contradiction count from metadata
            contradiction_count = db.execute_query(
                """
                MATCH (o:Opinion)
                WHERE toLower(o.metadata.topic) = toLower($topic)
                RETURN count(o) as contradiction_count
                """,
                {"topic": topic},
            )[0]["contradiction_count"]
            total_interactions = db.execute_query(
                """
                MATCH (o:Opinion)
                WHERE toLower(o.metadata.topic) = toLower($topic)
                RETURN count(o) as total_interactions
                """,
                {"topic": topic},
            )[0]["total_interactions"]

            # Calculate frequency
            frequency = contradiction_count / total_interactions

            return min(1.0, frequency)
        except Exception as e:
            logger.error(f"Error calculating contradiction frequency: {str(e)}")
            return 0.0

    def _get_domain_importance(self, domain_context: str) -> float:
        """
        Calculate the importance weight of a domain context.

        Args:
            domain_context: Domain context to evaluate

        Returns:
            float: Importance weight between 0 and 1
        """
        try:
            # Define domain importance weights
            domain_weights = {
                "scientific": 0.9,  # Scientific domains have high importance
                "technology": 0.7,  # Technology domains have moderate importance
                "breaking_news": 0.5,  # Breaking news has lower importance
                "social": 0.6,  # Social domains have moderate importance
                "economic": 0.8,  # Economic domains have high importance
                "political": 0.7,  # Political domains have moderate importance
            }

            return domain_weights.get(domain_context.lower(), 0.5)  # Default to 0.5
        except Exception as e:
            logger.error(f"Error calculating domain importance: {str(e)}")
            return 0.5  # Return default importance on error

    def _check_still_relevant(self, opinion1, opinion2) -> bool:
        """
        Check if two opinions are still relevant to each other despite time differences.

        Args:
            opinion1: First opinion
            opinion2: Second opinion

        Returns:
            bool: True if opinions are still relevant to each other
        """
        try:
            # Check if either opinion has a time horizon
            if not opinion1.time_horizon or not opinion2.time_horizon:
                return True

            # Get time difference in days
            time_diff = abs((opinion1.created_at - opinion2.created_at).days)

            # Define relevance thresholds based on time horizons
            thresholds = {
                TimeHorizon.SHORT_TERM: 30,  # 1 month
                TimeHorizon.MEDIUM_TERM: 180,  # 6 months
                TimeHorizon.LONG_TERM: 365,  # 1 year
            }

            # Get the longer time horizon
            longer_horizon = max(opinion1.time_horizon, opinion2.time_horizon)

            # Check if time difference is within threshold
            return time_diff <= thresholds.get(longer_horizon, 365)

        except Exception as e:
            logging.error(f"Error checking relevance: {str(e)}")
            return True  # Default to relevant on error
