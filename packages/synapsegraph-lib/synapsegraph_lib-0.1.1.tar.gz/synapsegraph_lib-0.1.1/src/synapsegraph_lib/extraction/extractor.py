"""
Extractor module for extracting knowledge from text using LangChain.

This module provides functionality to extract structured knowledge from
unstructured text, including entities, relationships, and statements.
"""

import logging
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime
import json

from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field, field_validator

from synapsegraph_lib.core.config import config, SourceType
from synapsegraph_lib.core.models import Entity, Belief, Source, Event, Concept
from synapsegraph_lib.core.database import Neo4jConnection
from synapsegraph_lib.utils.entity_resolution import (
    find_or_create_entity_with_resolution,
)

logger = logging.getLogger(__name__)


class ExtractedEntity(BaseModel):
    """Model for an extracted entity."""

    name: str = Field(description="The name of the entity")
    description: Optional[str] = Field(
        None, description="A brief description of the entity"
    )
    entity_type: str = Field(
        description="The type of entity (e.g., Person, Organization, Location)"
    )


class ExtractedBelief(BaseModel):
    """Model for an extracted belief statement."""

    statement: str = Field(description="The belief statement")
    confidence: float = Field(description="Confidence score (0.0 to 1.0)")
    entities: List[str] = Field(
        description="List of entity names involved in this belief"
    )

    @field_validator("confidence")
    @classmethod
    def check_confidence(cls, v: float) -> float:
        """Validate that confidence is between 0 and 1."""
        if not 0 <= v <= 1:
            raise ValueError("Confidence must be between 0 and 1")
        return v


class ExtractedEvent(BaseModel):
    """Model for an extracted event."""

    name: str = Field(description="The name of the event")
    description: Optional[str] = Field(None, description="A description of the event")
    timestamp: Optional[str] = Field(
        None, description="The timestamp of the event (ISO format if known)"
    )
    entities: List[str] = Field(
        description="List of entity names involved in this event"
    )


class ExtractedConcept(BaseModel):
    """Model for an extracted concept."""

    name: str = Field(description="The name of the concept")
    description: Optional[str] = Field(None, description="A description of the concept")


class ExtractionResult(BaseModel):
    """Model for the complete extraction result."""

    entities: List[ExtractedEntity] = Field(
        default_factory=list, description="Extracted entities"
    )
    beliefs: List[ExtractedBelief] = Field(
        default_factory=list, description="Extracted beliefs"
    )
    events: List[ExtractedEvent] = Field(
        default_factory=list, description="Extracted events"
    )
    concepts: List[ExtractedConcept] = Field(
        default_factory=list, description="Extracted concepts"
    )


class KnowledgeExtractor:
    """
    Class for extracting knowledge from text using LangChain and LLMs.
    """

    def __init__(
        self, llm_model: Optional[str] = None, temperature: Optional[float] = None
    ):
        """
        Initialize the knowledge extractor.

        Args:
            llm_model: LLM model to use (defaults to config)
            temperature: Temperature for LLM generation (defaults to config)
        """
        # Use a smaller, faster model for testing if none specified
        self.llm_model = llm_model or config.llm.model or "gpt-3.5-turbo"
        self.temperature = temperature or config.llm.temperature

        # Initialize LLM with verbose logging to track API calls
        logger.info(f"Initializing LLM with model: {self.llm_model}")
        self.llm = ChatOpenAI(
            model=self.llm_model,
            temperature=self.temperature,
            api_key=config.llm.api_key,
            verbose=True,
        )
        logger.info(f"LLM initialized successfully")

        # Initialize output parser
        self.parser = PydanticOutputParser(pydantic_object=ExtractionResult)

        # Initialize extraction prompt
        self.extraction_prompt = PromptTemplate(
            template="""
            You are an AI assistant specialized in extracting structured knowledge from text.
            Please analyze the following text and extract:
            
            1. Entities (people, organizations, locations, etc.)
            2. Belief statements with confidence scores
            3. Events with timestamps (if available)
            4. Concepts or abstract ideas
            
            Text to analyze:
            {text}
            
            {format_instructions}
            """,
            input_variables=["text"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )

        # Initialize extraction chain using the newer RunnableSequence pattern
        # This replaces the deprecated LLMChain
        self.extraction_chain = (
            {"text": RunnablePassthrough()} | self.extraction_prompt | self.llm
        )
        logger.info("KnowledgeExtractor initialized with extraction chain")

    def extract_knowledge(
        self,
        text: str,
        source_name: str,
        source_type: SourceType = SourceType.USER,
        source_trust_score: float = 0.5,
    ) -> Tuple[ExtractionResult, Source]:
        """
        Extract knowledge from text and create a source.

        Args:
            text: Text to extract knowledge from
            source_name: Name of the source
            source_type: Type of the source
            source_trust_score: Trust score for the source

        Returns:
            Tuple of (ExtractionResult, Source)
        """
        try:
            # Run extraction chain
            result = self.extraction_chain.invoke({"text": text})

            # Handle the newer LangChain response format
            # The response may be an AIMessage object instead of a string
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

            # Parse result
            try:
                extraction_result = self.parser.parse(result_content)
            except Exception as parse_error:
                logger.error(f"Failed to parse extraction result: {str(parse_error)}")
                logger.error(f"Raw result content: {result_content[:100]}...")

                # Attempt to manually parse JSON
                import json

                try:
                    json_data = json.loads(result_content)

                    # Create ExtractionResult from dictionary
                    extraction_result = ExtractionResult(
                        entities=json_data.get("entities", []),
                        beliefs=json_data.get("beliefs", []),
                        events=json_data.get("events", []),
                        concepts=json_data.get("concepts", []),
                    )
                    logger.info("Successfully manually parsed JSON result")
                except json.JSONDecodeError:
                    logger.error("Failed to manually parse JSON result")
                    extraction_result = ExtractionResult()

            # Create source
            source = Source(
                name=source_name,
                type=source_type,
                trust_score=source_trust_score,
                metadata={"original_text": text},
            )

            logger.info(
                f"Extracted {len(extraction_result.entities)} entities, "
                f"{len(extraction_result.beliefs)} beliefs, "
                f"{len(extraction_result.events)} events, "
                f"{len(extraction_result.concepts)} concepts "
                f"from source {source_name}"
            )

            return extraction_result, source
        except Exception as e:
            logger.error(f"Knowledge extraction failed: {str(e)}")
            # Return empty result
            return ExtractionResult(), Source(
                name=source_name, type=source_type, trust_score=source_trust_score
            )

    def convert_to_graph_objects(
        self, extraction_result: ExtractionResult, source: Source
    ) -> Dict[str, List[Any]]:
        """
        Convert extraction result to graph objects.

        Args:
            extraction_result: Extraction result
            source: Source of the information

        Returns:
            Dictionary of graph objects by type
        """
        entities = []
        beliefs = []
        events = []
        concepts = []

        # Convert entities
        for entity in extraction_result.entities:
            entities.append(
                Entity(
                    name=entity.name,
                    description=entity.description,
                    aliases=[],  # Will be populated during resolution
                    metadata={"entity_type": entity.entity_type},
                )
            )

        # Convert beliefs
        for belief in extraction_result.beliefs:
            beliefs.append(
                Belief(
                    statement=belief.statement,
                    confidence=belief.confidence,
                    metadata={"entities": belief.entities},
                )
            )

        # Convert events
        for event in extraction_result.events:
            timestamp = None
            if event.timestamp:
                try:
                    timestamp = datetime.fromisoformat(event.timestamp)
                except ValueError:
                    # If timestamp is not in ISO format, use current time
                    timestamp = datetime.now()
            else:
                timestamp = datetime.now()

            events.append(
                Event(
                    name=event.name,
                    description=event.description,
                    timestamp=timestamp,
                    metadata={"entities": event.entities},
                )
            )

        # Convert concepts
        for concept in extraction_result.concepts:
            concepts.append(Concept(name=concept.name, description=concept.description))

        return {
            "entities": entities,
            "beliefs": beliefs,
            "events": events,
            "concepts": concepts,
            "source": [source],
        }

    def save_to_graph(
        self, db: Neo4jConnection, graph_objects: Dict[str, List[Any]]
    ) -> bool:
        """
        Save extracted knowledge to the graph database.

        Args:
            db: Neo4j connection
            graph_objects: Dictionary of graph objects by type

        Returns:
            True if successful, False otherwise
        """
        try:
            # Save source first
            for source in graph_objects.get("source", []):
                if not source.save(db):
                    logger.error(f"Failed to save source: {source.name}")
                    return False

            # Process and save entities with resolution
            resolved_entities = {}  # Map of entity name to resolved entity
            for entity in graph_objects.get("entities", []):
                # Use entity resolution to find or create entity
                resolved_entity = find_or_create_entity_with_resolution(
                    db, entity.name, entity.description, generate_aliases=True
                )

                if resolved_entity:
                    # Update metadata if needed
                    if "entity_type" in entity.metadata:
                        if "entity_type" not in resolved_entity.metadata:
                            resolved_entity.metadata["entity_type"] = entity.metadata[
                                "entity_type"
                            ]
                            resolved_entity.save(db)

                    # Store the resolved entity for later use
                    resolved_entities[entity.name] = resolved_entity
                else:
                    logger.error(f"Failed to resolve entity: {entity.name}")

            # Save concepts
            for concept in graph_objects.get("concepts", []):
                if not concept.save(db):
                    logger.error(f"Failed to save concept: {concept.name}")
                    continue

            # Save events and link to resolved entities
            for event in graph_objects.get("events", []):
                if not event.save(db):
                    logger.error(f"Failed to save event: {event.name}")
                    continue

                # Link events to entities
                entity_names = event.metadata.get("entities", [])
                for entity_name in entity_names:
                    # Try to find the resolved entity
                    if entity_name in resolved_entities:
                        resolved_entity = resolved_entities[entity_name]
                    else:
                        # If not found in our resolved entities, try to find by name or alias
                        resolved_entity = Entity.find_by_name_or_alias(db, entity_name)

                    if resolved_entity:
                        # Create relationship between event and entity
                        query = """
                        MATCH (e:Event {name: $event_name})
                        MATCH (ent:Entity {name: $entity_name})
                        MERGE (e)-[r:INVOLVES]->(ent)
                        ON CREATE SET r.created_at = datetime($created_at)
                        ON MATCH SET r.updated_at = datetime($updated_at)
                        RETURN r
                        """

                        params = {
                            "event_name": event.name,
                            "entity_name": resolved_entity.name,
                            "created_at": datetime.now().isoformat(),
                            "updated_at": datetime.now().isoformat(),
                        }

                        try:
                            db.execute_write_transaction(query, params)
                        except Exception as e:
                            logger.error(
                                f"Failed to link event to entity: {event.name} -> {resolved_entity.name}: {str(e)}"
                            )

            # Save beliefs and link to entities and source
            for belief in graph_objects.get("beliefs", []):
                if not belief.save(db):
                    logger.error(f"Failed to save belief: {belief.statement}")
                    continue

                # Link to source
                if graph_objects.get("source"):
                    source = graph_objects["source"][0]
                    if not belief.link_to_source(db, source):
                        logger.error(
                            f"Failed to link belief to source: {belief.statement} -> {source.name}"
                        )

                # Link to resolved entities
                entity_names = belief.metadata.get("entities", [])
                for entity_name in entity_names:
                    # Try to find the resolved entity
                    if entity_name in resolved_entities:
                        resolved_entity = resolved_entities[entity_name]
                    else:
                        # If not found in our resolved entities, try to find by name or alias
                        resolved_entity = Entity.find_by_name_or_alias(db, entity_name)

                    if resolved_entity:
                        if not belief.link_to_entity(db, resolved_entity):
                            logger.error(
                                f"Failed to link belief to entity: {belief.statement} -> {resolved_entity.name}"
                            )

            logger.info("Successfully saved extracted knowledge to graph")
            return True
        except Exception as e:
            logger.error(f"Failed to save extracted knowledge to graph: {str(e)}")
            return False
