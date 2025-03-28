"""
Entity resolution utilities for handling entity aliasing and deduplication.

This module provides functions to help resolve entity references, detect duplicates,
and manage entity aliases.
"""

import logging
from typing import List, Dict, Optional, Tuple, Any, Set
import datetime
import re
from difflib import SequenceMatcher

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

from synapsegraph_lib.core.config import config
from synapsegraph_lib.core.models import Entity
from synapsegraph_lib.core.database import Neo4jConnection

logger = logging.getLogger(__name__)


def calculate_similarity(str1: str, str2: str) -> float:
    """
    Calculate string similarity using SequenceMatcher.

    Args:
        str1: First string
        str2: Second string

    Returns:
        Similarity score between 0.0 and 1.0
    """
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()


def find_potential_duplicates(
    db: Neo4jConnection, similarity_threshold: float = 0.8
) -> List[Tuple[Entity, Entity, float]]:
    """
    Find potential duplicate entities in the database.

    Args:
        db: Neo4j connection
        similarity_threshold: Minimum similarity score to consider entities as potential duplicates

    Returns:
        List of tuples containing (entity1, entity2, similarity_score)
    """
    # Get all entities
    query = "MATCH (e:Entity) RETURN e"

    try:
        results = db.execute_query(query, {}, fetch_all=True)
        entities = []

        for result in results:
            if "e" in result:
                entity_data = dict(result["e"])
                entities.append(Entity.from_dict(entity_data))

        # Compare entities for similarity
        potential_duplicates = []
        for i, entity1 in enumerate(entities):
            for entity2 in entities[i + 1 :]:
                # Check name similarity
                similarity = calculate_similarity(entity1.name, entity2.name)

                # Also check aliases
                for alias1 in entity1.aliases:
                    for alias2 in entity2.aliases:
                        alias_similarity = calculate_similarity(alias1, alias2)
                        similarity = max(similarity, alias_similarity)

                    # Check alias against name
                    name_alias_similarity = calculate_similarity(alias1, entity2.name)
                    similarity = max(similarity, name_alias_similarity)

                for alias2 in entity2.aliases:
                    # Check name against alias
                    name_alias_similarity = calculate_similarity(entity1.name, alias2)
                    similarity = max(similarity, name_alias_similarity)

                if similarity >= similarity_threshold:
                    potential_duplicates.append((entity1, entity2, similarity))

        return potential_duplicates

    except Exception as e:
        logger.error(f"Failed to find potential duplicates: {str(e)}")
        return []


def find_context_aware_duplicates(
    db: Neo4jConnection, similarity_threshold: float = 0.9
) -> List[Tuple[Entity, Entity, float, bool]]:
    """
    Find potential duplicate entities with context awareness.

    This improved version checks not only for name/alias similarity but also
    for context overlap between entities to avoid incorrect merges.

    Args:
        db: Neo4j connection
        similarity_threshold: Minimum similarity score to consider entities as potential duplicates

    Returns:
        List of tuples containing (entity1, entity2, similarity_score, has_context_overlap)
    """
    # Get all entities
    query = "MATCH (e:Entity) RETURN e"

    try:
        results = db.execute_query(query, {}, fetch_all=True)
        entities = []

        for result in results:
            if "e" in result:
                entity_data = dict(result["e"])
                entities.append(Entity.from_dict(entity_data))

        # Compare entities for similarity
        potential_duplicates = []
        for i, entity1 in enumerate(entities):
            for entity2 in entities[i + 1 :]:
                # Check name similarity
                similarity = calculate_similarity(entity1.name, entity2.name)

                # Also check aliases
                for alias1 in entity1.aliases:
                    for alias2 in entity2.aliases:
                        alias_similarity = calculate_similarity(alias1, alias2)
                        similarity = max(similarity, alias_similarity)

                    # Check alias against name
                    name_alias_similarity = calculate_similarity(alias1, entity2.name)
                    similarity = max(similarity, name_alias_similarity)

                for alias2 in entity2.aliases:
                    # Check name against alias
                    name_alias_similarity = calculate_similarity(entity1.name, alias2)
                    similarity = max(similarity, name_alias_similarity)

                # Only proceed if similarity is above threshold
                if similarity >= similarity_threshold:
                    # Check for context overlap
                    has_context_overlap = check_context_overlap(db, entity1, entity2)
                    potential_duplicates.append(
                        (entity1, entity2, similarity, has_context_overlap)
                    )

        return potential_duplicates

    except Exception as e:
        logger.error(f"Failed to find context-aware duplicates: {str(e)}")
        return []


def check_context_overlap(
    db: Neo4jConnection, entity1: Entity, entity2: Entity
) -> bool:
    """
    Check if two entities have overlapping contexts.

    Context overlap is determined by:
    1. Shared relationships to the same entities
    2. Shared beliefs
    3. Shared context tags
    4. Temporal co-occurrence

    Args:
        db: Neo4j connection
        entity1: First entity
        entity2: Second entity

    Returns:
        True if entities have overlapping contexts, False otherwise
    """
    try:
        # Check for shared context tags
        entity1_tags = set(entity1.context_tags)
        entity2_tags = set(entity2.context_tags)
        shared_tags = entity1_tags.intersection(entity2_tags)

        if shared_tags:
            logger.debug(f"Entities share context tags: {shared_tags}")
            return True

        # Check for shared relationships
        query = """
        MATCH (e1:Entity {name: $name1})
        MATCH (e2:Entity {name: $name2})
        MATCH (e1)-[r1]->(n)
        MATCH (e2)-[r2]->(n)
        RETURN count(n) as shared_relationships
        """

        params = {"name1": entity1.name, "name2": entity2.name}
        result = db.execute_query_single(query, params)

        if result and result.get("shared_relationships", 0) > 0:
            logger.debug(
                f"Entities share {result['shared_relationships']} relationships"
            )
            return True

        # Check for shared beliefs
        query = """
        MATCH (e1:Entity {name: $name1})-[:MENTIONED_IN]->(b1:Belief)
        MATCH (e2:Entity {name: $name2})-[:MENTIONED_IN]->(b2:Belief)
        WHERE b1.statement = b2.statement
        RETURN count(b1) as shared_beliefs
        """

        result = db.execute_query_single(query, params)

        if result and result.get("shared_beliefs", 0) > 0:
            logger.debug(f"Entities share {result['shared_beliefs']} beliefs")
            return True

        # Check for temporal co-occurrence (entities mentioned in events within same timeframe)
        query = """
        MATCH (e1:Entity {name: $name1})-[:PARTICIPATED_IN]->(ev1:Event)
        MATCH (e2:Entity {name: $name2})-[:PARTICIPATED_IN]->(ev2:Event)
        WHERE abs(duration.between(ev1.timestamp, ev2.timestamp).days) < 30
        RETURN count(ev1) as temporal_overlap
        """

        result = db.execute_query_single(query, params)

        if result and result.get("temporal_overlap", 0) > 0:
            logger.debug(
                f"Entities have temporal overlap in {result['temporal_overlap']} events"
            )
            return True

        # No context overlap found
        return False

    except Exception as e:
        logger.error(f"Error checking context overlap: {str(e)}")
        # Default to False to prevent incorrect merges
        return False


def context_aware_merge_entities(
    db: Neo4jConnection, entity1: Entity, entity2: Entity, keep_entity1: bool = True
) -> Optional[Entity]:
    """
    Merge two entities with context awareness.

    This function first checks if the entities have overlapping contexts before merging.

    Args:
        db: Neo4j connection
        entity1: First entity
        entity2: Second entity
        keep_entity1: Whether to keep entity1 (True) or entity2 (False)

    Returns:
        Merged entity if successful, None otherwise
    """
    try:
        # Calculate similarity
        similarity = calculate_similarity(entity1.name, entity2.name)

        # Check for context overlap
        has_context_overlap = check_context_overlap(db, entity1, entity2)

        # Only merge if similarity is high and contexts overlap
        if similarity > 0.9 and has_context_overlap:
            logger.info(
                f"Context overlap confirmed for {entity1.name} and {entity2.name}"
            )
            return merge_entities(db, entity1, entity2, keep_entity1)
        else:
            if similarity <= 0.9:
                logger.info(f"Similarity too low for merging: {similarity:.2f}")
            if not has_context_overlap:
                logger.info(
                    f"No context overlap between {entity1.name} and {entity2.name}"
                )
            return None

    except Exception as e:
        logger.error(f"Failed to perform context-aware merge: {str(e)}")
        return None


def merge_entities(
    db: Neo4jConnection, entity1: Entity, entity2: Entity, keep_entity1: bool = True
) -> Optional[Entity]:
    """
    Merge two entities, keeping one and updating all relationships to point to it.

    Args:
        db: Neo4j connection
        entity1: First entity
        entity2: Second entity
        keep_entity1: Whether to keep entity1 (True) or entity2 (False)

    Returns:
        Merged entity if successful, None otherwise
    """
    try:
        # Determine which entity to keep and which to merge
        keep_entity = entity1 if keep_entity1 else entity2
        merge_entity = entity2 if keep_entity1 else entity1

        # Combine aliases
        combined_aliases = list(set(keep_entity.aliases + merge_entity.aliases))

        # Add the merged entity's name as an alias if it's not already the kept entity's name
        if (
            merge_entity.name != keep_entity.name
            and merge_entity.name not in combined_aliases
        ):
            combined_aliases.append(merge_entity.name)

        # Update the kept entity with combined aliases
        keep_entity.aliases = combined_aliases

        # Merge metadata
        for key, value in merge_entity.metadata.items():
            if key not in keep_entity.metadata:
                keep_entity.metadata[key] = value

        # Update the kept entity in the database
        if not keep_entity.save(db):
            logger.error(f"Failed to update kept entity {keep_entity.name}")
            return None

        # Update all relationships from the merged entity to point to the kept entity
        query = """
        MATCH (old:Entity {name: $old_name})
        MATCH (keep:Entity {name: $keep_name})
        MATCH (old)-[r]->(n)
        WHERE NOT (keep)-[:BELIEVES]->(n)
        CREATE (keep)-[r2:BELIEVES]->(n)
        SET r2 = r
        WITH old, keep
        MATCH (n)-[r]->(old)
        WHERE NOT (n)-[:BELIEVES]->(keep)
        CREATE (n)-[r2:BELIEVES]->(keep)
        SET r2 = r
        WITH old
        DETACH DELETE old
        """

        params = {"old_name": merge_entity.name, "keep_name": keep_entity.name}

        if db.execute_write_transaction(query, params):
            logger.info(
                f"Successfully merged entity {merge_entity.name} into {keep_entity.name}"
            )
            return keep_entity
        else:
            logger.error(f"Failed to merge entity relationships")
            return None

    except Exception as e:
        logger.error(f"Failed to merge entities: {str(e)}")
        return None


def suggest_entity_aliases(
    db: Neo4jConnection, entity_name: str, llm_model: Optional[str] = None
) -> List[str]:
    """
    Suggest potential aliases for an entity using an LLM.

    Args:
        db: Neo4j connection
        entity_name: Entity name
        llm_model: Optional LLM model to use

    Returns:
        List of suggested aliases
    """
    try:
        # Get LLM model from config if not provided
        if not llm_model:
            from synapsegraph_lib.core.config import config

            llm_model = config.llm.model

        # Initialize LLM
        from langchain_openai import ChatOpenAI
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain

        llm = ChatOpenAI(
            model=llm_model,
            temperature=0.3,  # Lower temperature for more predictable outputs
        )

        # Create prompt
        prompt = PromptTemplate.from_template(
            """
            Entity: {entity_name}
            
            Please provide a list of potential aliases or alternative names that might refer to this same entity.
            Format your response as a comma-separated list of aliases.
            
            For example, for "Federal Bureau of Investigation", you might respond with:
            FBI, The Bureau, Federal Bureau
            
            For "United Nations", you might respond with:
            UN, U.N., United Nations Organization, UNO
            
            Aliases for {entity_name}:
            """
        )

        # Create and run chain
        chain = LLMChain(llm=llm, prompt=prompt)
        result = chain.invoke({"entity_name": entity_name})

        # Extract text from response
        result_text = ""
        if hasattr(result, "content"):
            result_text = result.content
        elif hasattr(result, "text"):
            result_text = result.text
        else:
            result_text = str(result)

        # Handle common acronyms for proper capitalization
        common_acronyms = {
            "fbi": "FBI",
            "cia": "CIA",
            "nasa": "NASA",
            "un": "UN",
            "u.n.": "U.N.",
            "nato": "NATO",
            "who": "WHO",
            "fda": "FDA",
            "epa": "EPA",
            "doj": "DOJ",
        }

        # Process aliases with consistent rules
        aliases = []
        for raw_alias in result_text.split(","):
            alias = raw_alias.strip()

            # Skip empty or malformed entries
            if not alias or alias.lower() == entity_name.lower():
                continue

            # Skip entries that look like part of a dictionary or JSON structure
            if any(
                x in alias
                for x in ["'text':", "'entity_name':", ":", "{", "}", "[", "]"]
            ):
                continue

            # Skip entries that start with common keys from response structures
            if any(
                alias.lower().startswith(x) for x in ["text", "content", "entity_name"]
            ):
                continue

            # Handle capitalization appropriately
            alias_lower = alias.lower()
            if alias_lower in common_acronyms:
                aliases.append(common_acronyms[alias_lower])
            else:
                # Use title case for regular names (e.g., "The Bureau")
                aliases.append(alias.title())

        logger.info(f"Generated {len(aliases)} potential aliases for {entity_name}")
        return aliases

    except Exception as e:
        logger.error(f"Failed to suggest aliases for entity {entity_name}: {str(e)}")
        return []


def find_or_create_entity_with_resolution(
    db: Neo4jConnection,
    entity_name: str,
    description: Optional[str] = None,
    generate_aliases: bool = True,
) -> Optional[Entity]:
    """
    Find an entity by name or alias, or create it if it doesn't exist.
    Optionally generates aliases for new entities.

    Args:
        db: Neo4j connection
        entity_name: Entity name
        description: Entity description
        generate_aliases: Whether to generate aliases for new entities

    Returns:
        Entity object if found or created, None otherwise
    """
    try:
        # First try to find by name or alias
        entity = Entity.find_by_name_or_alias(db, entity_name)

        if entity:
            logger.info(f"Found existing entity: {entity.name}")
            return entity

        # Entity doesn't exist, create it
        entity = Entity(
            name=entity_name, description=description, aliases=[], metadata={}
        )

        # Generate aliases if requested
        if generate_aliases:
            aliases = suggest_entity_aliases(db, entity_name)
            entity.aliases = aliases

        # Save the entity
        if entity.save(db):
            logger.info(
                f"Created new entity: {entity.name} with {len(entity.aliases)} aliases"
            )
            return entity
        else:
            logger.error(f"Failed to create entity: {entity_name}")
            return None

    except Exception as e:
        logger.error(f"Error in find_or_create_entity_with_resolution: {str(e)}")
        return None
