"""
Conflict Resolution with LLM (CRDL) module for SynapseGraph.

This module implements an advanced conflict resolution approach using LLMs
to analyze and resolve contradictions in the knowledge graph.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field

from synapsegraph_lib.core.config import config, ConflictStatus
from synapsegraph_lib.core.models import Opinion, ConflictResolution
from synapsegraph_lib.core.database import Neo4jConnection

logger = logging.getLogger(__name__)


class ConflictAnalysis(BaseModel):
    """Model for LLM-based conflict analysis results."""

    conflict_type: str = Field(
        description="Type of conflict (e.g., logical, temporal, factual)"
    )
    severity: float = Field(description="Severity score (0.0 to 1.0)")
    resolution_strategy: str = Field(description="Recommended resolution strategy")
    reasoning: str = Field(description="Detailed reasoning for the resolution")
    confidence: float = Field(description="Confidence in the resolution (0.0 to 1.0)")
    metadata: Dict[str, Any] = Field(
        description="Additional metadata about the conflict"
    )


class ConflictResolutionLLM:
    """
    Implements LLM-based conflict resolution using the CRDL approach.
    """

    def __init__(
        self, llm_model: Optional[str] = None, temperature: Optional[float] = None
    ):
        """
        Initialize the CRDL-based conflict resolver.

        Args:
            llm_model: LLM model to use (defaults to config)
            temperature: Temperature for LLM generation (defaults to config)
        """
        self.llm_model = llm_model or config.llm.model
        self.temperature = temperature or config.llm.temperature

        # Initialize LLM
        self.llm = ChatOpenAI(
            model=self.llm_model,
            temperature=self.temperature,
            api_key=config.llm.api_key,
        )

        # Create analysis prompt template
        self.analysis_prompt = PromptTemplate(
            template="""
            Analyze the following conflict between opinions in a knowledge graph:

            OPINION 1:
            Statement: {opinion1_statement}
            Confidence: {opinion1_confidence}
            Stance: {opinion1_stance}
            Context: {opinion1_context}

            OPINION 2:
            Statement: {opinion2_statement}
            Confidence: {opinion2_confidence}
            Stance: {opinion2_stance}
            Context: {opinion2_context}

            ADDITIONAL CONTEXT:
            {additional_context}

            Analyze this conflict and provide:
            1. The type of conflict (logical, temporal, factual)
            2. A severity score (0.0 to 1.0)
            3. A recommended resolution strategy
            4. Detailed reasoning for the resolution
            5. Confidence in the resolution (0.0 to 1.0)
            6. Any relevant metadata

            Consider:
            - Temporal validity of the opinions
            - Source reliability and trust scores
            - Logical consistency
            - Domain-specific context
            - Potential biases or limitations

            {format_instructions}
            """,
            input_variables=[
                "opinion1_statement",
                "opinion1_confidence",
                "opinion1_stance",
                "opinion1_context",
                "opinion2_statement",
                "opinion2_confidence",
                "opinion2_stance",
                "opinion2_context",
                "additional_context",
                "format_instructions",
            ],
        )

        # Initialize analysis chain
        self.analysis_chain = (
            {
                "opinion1_statement": lambda x: x["opinion1"].statement,
                "opinion1_confidence": lambda x: str(x["opinion1"].confidence),
                "opinion1_stance": lambda x: x["opinion1"].stance.value,
                "opinion1_context": lambda x: x["opinion1_context"],
                "opinion2_statement": lambda x: x["opinion2"].statement,
                "opinion2_confidence": lambda x: str(x["opinion2"].confidence),
                "opinion2_stance": lambda x: x["opinion2"].stance.value,
                "opinion2_context": lambda x: x["opinion2_context"],
                "additional_context": lambda x: x["additional_context"],
                "format_instructions": lambda x: x["format_instructions"],
            }
            | self.analysis_prompt
            | self.llm
        )

    def analyze_conflict(
        self,
        opinion1: Opinion,
        opinion2: Opinion,
        opinion1_context: str = "",
        opinion2_context: str = "",
        additional_context: str = "",
    ) -> ConflictAnalysis:
        """
        Analyze a conflict between two opinions using LLM.

        Args:
            opinion1: First opinion
            opinion2: Second opinion
            opinion1_context: Additional context for first opinion
            opinion2_context: Additional context for second opinion
            additional_context: Any additional context about the conflict

        Returns:
            ConflictAnalysis object containing the analysis results
        """
        try:
            # Prepare input for the analysis chain
            chain_input = {
                "opinion1": opinion1,
                "opinion2": opinion2,
                "opinion1_context": opinion1_context,
                "opinion2_context": opinion2_context,
                "additional_context": additional_context,
                "format_instructions": ConflictAnalysis.model_json_schema(),
            }

            # Run the analysis chain
            result = self.analysis_chain.invoke(chain_input)

            # Parse the result into a ConflictAnalysis object
            analysis = ConflictAnalysis.model_validate_json(result.content)
            return analysis

        except Exception as e:
            logger.error(f"Failed to analyze conflict: {str(e)}")
            raise

    def resolve_conflict(
        self,
        db: Neo4jConnection,
        conflict_resolution: ConflictResolution,
        analysis: ConflictAnalysis,
    ) -> bool:
        """
        Resolve a conflict based on LLM analysis.

        Args:
            db: Neo4j database connection
            conflict_resolution: ConflictResolution object to update
            analysis: ConflictAnalysis object containing the analysis results

        Returns:
            True if resolution was successful, False otherwise
        """
        try:
            # Update the conflict resolution with analysis results
            conflict_resolution.status = ConflictStatus.RESOLVED
            conflict_resolution.resolution_details = analysis.reasoning
            conflict_resolution.metadata.update(
                {
                    "resolved_at": datetime.now().isoformat(),
                    "resolution_type": analysis.conflict_type,
                    "resolution_severity": analysis.severity,
                    "resolution_confidence": analysis.confidence,
                    "resolution_strategy": analysis.resolution_strategy,
                    **analysis.metadata,
                }
            )

            # Save the updated conflict resolution
            if not conflict_resolution.save(db):
                logger.error("Failed to save conflict resolution")
                return False

            logger.info(f"Resolved conflict: {conflict_resolution.topic}")
            return True

        except Exception as e:
            logger.error(f"Failed to resolve conflict: {str(e)}")
            return False
