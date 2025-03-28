"""
Ingestor module for ingesting data from various sources.

This module provides functionality to ingest data from various sources,
including user input, web content, and APIs.
"""

import logging
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime
import json
from pathlib import Path
import gc  # For garbage collection
import time  # For adding delays between API calls

from synapsegraph_lib.core.config import config, SourceType
from synapsegraph_lib.core.models import Neo4jConnection
from synapsegraph_lib.extraction.extractor import KnowledgeExtractor
from synapsegraph_lib.synthesis.opinion_formation import OpinionSynthesizer
from synapsegraph_lib.synthesis.belief_manager import BeliefManager
from synapsegraph_lib.temporal.temporal_management import TemporalManager

logger = logging.getLogger(__name__)


class Ingestor:
    """
    Base class for ingesting data from various sources.
    """

    def __init__(self, db: Neo4jConnection):
        """
        Initialize the ingestor.

        Args:
            db: Neo4j connection
        """
        self.db = db
        self.extractor = KnowledgeExtractor()
        self.temporal_manager = TemporalManager()
        self.synthesizer = OpinionSynthesizer(self.temporal_manager)
        self.belief_manager = BeliefManager(db)

    def ingest(
        self,
        content: str,
        source_name: str,
        source_type: SourceType,
        source_trust_score: float = 0.5,
    ) -> bool:
        """
        Ingest content from a source.

        Args:
            content: Content to ingest
            source_name: Name of the source
            source_type: Type of the source
            source_trust_score: Trust score for the source

        Returns:
            True if successful, False otherwise
        """
        try:
            # Memory optimization: Limit content size
            if len(content) > 10000:
                logger.warning("Content too large, truncating to 10000 characters")
                content = content[:10000]

            # Extract knowledge from content
            logger.info(f"Extracting knowledge from source: {source_name}")
            start_time = time.time()

            extraction_result, source = self.extractor.extract_knowledge(
                content, source_name, source_type, source_trust_score
            )

            logger.info(
                f"Knowledge extraction completed in {time.time() - start_time:.2f} seconds"
            )

            # Memory optimization: Force garbage collection after extraction
            gc.collect()

            # Convert to graph objects
            logger.info("Converting extraction results to graph objects")
            graph_objects = self.extractor.convert_to_graph_objects(
                extraction_result, source
            )

            # Process beliefs using the belief manager
            processed_beliefs = []
            for belief in graph_objects.get("beliefs", []):
                # Find or update the belief
                processed_belief = self.belief_manager.find_or_update_belief(
                    statement=belief.statement,
                    confidence=belief.confidence,
                    source=source,
                    category=belief.metadata.get("category", ""),
                    speculative=False,  # Default to non-speculative
                )

                if processed_belief:
                    processed_beliefs.append(processed_belief)

                    # Link to entities
                    entity_names = belief.metadata.get("entities", [])
                    for entity_name in entity_names:
                        # Try to find the entity
                        from synapsegraph_lib.utils.entity_resolution import (
                            find_or_create_entity_with_resolution,
                        )

                        entity = find_or_create_entity_with_resolution(
                            self.db, entity_name, generate_aliases=True
                        )

                        if entity:
                            processed_belief.link_to_entity(self.db, entity)

            # Replace the beliefs in graph_objects with the processed ones
            graph_objects["beliefs"] = processed_beliefs

            # Memory optimization: Force garbage collection again
            gc.collect()

            # Save other objects to graph (entities, events, concepts)
            logger.info("Saving extracted knowledge to the graph database")
            success = self.extractor.save_to_graph(self.db, graph_objects)

            if success:
                logger.info(f"Successfully ingested content from {source_name}")

                # Extract topics from beliefs for opinion synthesis
                topics = self._extract_topics_from_beliefs(processed_beliefs)

                # Synthesize opinions for each topic
                for topic in topics:
                    opinion = self.synthesizer.synthesize_opinion(self.db, topic)
                    if opinion:
                        logger.info(
                            f"Synthesized opinion on topic '{topic}': {opinion.statement}"
                        )
                    else:
                        logger.warning(
                            f"Failed to synthesize opinion on topic '{topic}'"
                        )

                # Memory optimization: Clear processed data
                extraction_result = None
                graph_objects = None
                processed_beliefs = None
                gc.collect()

                return True
            else:
                logger.error(f"Failed to ingest content from {source_name}")
                return False
        except Exception as e:
            logger.error(f"Ingestion failed: {str(e)}")
            import traceback

            logger.error(traceback.format_exc())
            return False

    def _extract_topics_from_beliefs(self, beliefs: List[Any]) -> List[str]:
        """
        Extract topics from beliefs for opinion synthesis.

        Args:
            beliefs: List of Belief objects

        Returns:
            List of topics
        """
        # This is a simplified approach - in a real system, you would use
        # more sophisticated NLP techniques to extract topics

        topics = set()

        for belief in beliefs:
            # Split statement into words and consider words longer than 4 characters as potential topics
            words = belief.statement.split()
            for word in words:
                word = word.strip().lower()
                if len(word) > 4 and word not in [
                    "about",
                    "there",
                    "their",
                    "would",
                    "could",
                    "should",
                ]:
                    topics.add(word)

        # Limit to top 5 topics to avoid too many opinion synthesis operations
        return list(topics)[:5]


class UserInputIngestor(Ingestor):
    """
    Ingestor for user input.
    """

    def ingest_user_input(self, user_input: str, user_id: str = "user") -> bool:
        """
        Ingest input from a user.

        Args:
            user_input: User input text
            user_id: User identifier

        Returns:
            True if successful, False otherwise
        """
        source_name = f"User_{user_id}"
        return self.ingest(user_input, source_name, SourceType.USER, 0.7)


class WebContentIngestor(Ingestor):
    """
    Ingestor for web content.
    """

    def ingest_web_content(
        self, content: str, url: str, trust_score: float = 0.5
    ) -> bool:
        """
        Ingest content from a web page.

        Args:
            content: Web page content
            url: URL of the web page
            trust_score: Trust score for the source

        Returns:
            True if successful, False otherwise
        """
        source_name = f"Web_{url}"
        return self.ingest(content, source_name, SourceType.NEWS, trust_score)


class APIIngestor(Ingestor):
    """
    Ingestor for API data.
    """

    def ingest_api_data(
        self, data: Dict[str, Any], api_name: str, trust_score: float = 0.6
    ) -> bool:
        """
        Ingest data from an API.

        Args:
            data: API data (will be converted to JSON string)
            api_name: Name of the API
            trust_score: Trust score for the source

        Returns:
            True if successful, False otherwise
        """
        content = json.dumps(data, indent=2)
        source_name = f"API_{api_name}"
        return self.ingest(content, source_name, SourceType.API, trust_score)


class ResearchIngestor(Ingestor):
    """
    Ingestor for research papers and articles.
    """

    def ingest_research(
        self,
        content: str,
        title: str,
        authors: List[str],
        publication: Optional[str] = None,
        trust_score: float = 0.8,
    ) -> bool:
        """
        Ingest content from a research paper or article.

        Args:
            content: Research paper content
            title: Title of the paper
            authors: List of authors
            publication: Publication name
            trust_score: Trust score for the source

        Returns:
            True if successful, False otherwise
        """
        metadata = {"title": title, "authors": authors}

        if publication:
            metadata["publication"] = publication

        source_name = f"Research_{title}"

        # Add metadata to content for better extraction
        enhanced_content = f"Title: {title}\nAuthors: {', '.join(authors)}\n"
        if publication:
            enhanced_content += f"Publication: {publication}\n"
        enhanced_content += f"\n{content}"

        return self.ingest(
            enhanced_content, source_name, SourceType.RESEARCH, trust_score
        )


class BatchIngestor(Ingestor):
    """
    Ingestor for batch processing multiple sources.
    """

    def ingest_batch(self, items: List[Dict[str, Any]]) -> Dict[str, bool]:
        """
        Ingest multiple items in batch.

        Args:
            items: List of items to ingest, each with:
                - content: Content to ingest
                - source_name: Name of the source
                - source_type: Type of the source (as string)
                - source_trust_score: Trust score for the source

        Returns:
            Dictionary mapping source names to success status
        """
        results = {}

        for item in items:
            content = item.get("content", "")
            source_name = item.get("source_name", f"Batch_{datetime.now().isoformat()}")

            # Convert source_type string to enum
            source_type_str = item.get("source_type", "USER")
            try:
                source_type = SourceType[source_type_str.upper()]
            except (KeyError, AttributeError):
                source_type = SourceType.USER

            source_trust_score = item.get("source_trust_score", 0.5)

            success = self.ingest(content, source_name, source_type, source_trust_score)
            results[source_name] = success

        return results


class FileIngestor(Ingestor):
    """
    Ingestor for content from files.

    This class handles ingestion of content from local files,
    determining appropriate trust scores and topics.
    """

    def ingest_content(
        self,
        content: str,
        source_url: str = "",
        source_name: str = "",
        topics: List[str] = None,
        trust_score: float = 0.6,
    ) -> bool:
        """
        Ingest content from a file.

        Args:
            content: Content to ingest
            source_url: URL or file path of the source
            source_name: Name of the file source
            topics: List of topics associated with the content
            trust_score: Trust score for the source (0.0 to 1.0)

        Returns:
            True if ingestion was successful, False otherwise
        """
        if not source_name:
            if source_url:
                # Extract filename from URL/path
                source_name = f"File: {Path(source_url).name}"
            else:
                source_name = "Unknown File"

        logger.info(f"Ingesting content from file source: {source_name}")

        # Call the base ingest method with file-specific parameters
        return self.ingest(
            content=content,
            source_name=source_name,
            source_type=SourceType.FILE,
            source_trust_score=trust_score,
        )
