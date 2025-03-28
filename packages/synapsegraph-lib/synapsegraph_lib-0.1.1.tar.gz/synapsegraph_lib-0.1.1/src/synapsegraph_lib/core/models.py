"""
Models module defining the graph data models for Synapse.

This module provides dataclasses that represent the nodes and relationships
in the Synapse knowledge graph, along with methods for CRUD operations.
"""

import logging
import datetime
import json
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any, Union, Set
from uuid import uuid4
import inspect

from synapsegraph_lib.core.config import (
    SourceType,
    OpinionStance,
    ConflictStatus,
    TimeHorizon,
)
from synapsegraph_lib.core.database import Neo4jConnection

logger = logging.getLogger(__name__)


@dataclass
class Node:
    """Base class for all graph nodes."""

    uid: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = field(default_factory=datetime.datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the node to a dictionary for Neo4j operations."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Node":
        """Create a node instance from a dictionary."""
        # Filter out keys that are not in the dataclass
        valid_keys = {field.name for field in cls.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}

        # Convert string dates to datetime objects
        if "created_at" in filtered_data and isinstance(
            filtered_data["created_at"], str
        ):
            filtered_data["created_at"] = datetime.datetime.fromisoformat(
                filtered_data["created_at"]
            )
        if "updated_at" in filtered_data and isinstance(
            filtered_data["updated_at"], str
        ):
            filtered_data["updated_at"] = datetime.datetime.fromisoformat(
                filtered_data["updated_at"]
            )

        # Convert metadata from JSON string to dictionary if needed
        if "metadata" in filtered_data and isinstance(filtered_data["metadata"], str):
            try:
                filtered_data["metadata"] = json.loads(filtered_data["metadata"])
            except json.JSONDecodeError:
                filtered_data["metadata"] = {}

        return cls(**filtered_data)


@dataclass
class Entity(Node):
    """
    Entity node representing a person, organization, or other named entity.
    """

    name: str = ""
    description: Optional[str] = None
    canonical: bool = False  # Whether this is the preferred standardized name
    aliases: List[str] = field(default_factory=list)
    embedding: Optional[str] = None
    context_tags: List[str] = field(
        default_factory=list
    )  # Tags providing additional context
    metadata: Dict[str, Any] = field(default_factory=dict)

    def save(self, db: Neo4jConnection) -> bool:
        """
        Save the entity to the database.

        Args:
            db: Neo4j connection

        Returns:
            True if successful, False otherwise
        """
        query = """
        MERGE (e:Entity {name: $name})
        ON CREATE SET 
            e.uid = $uid,
            e.created_at = datetime($created_at),
            e.description = $description,
            e.canonical = $canonical,
            e.aliases = $aliases,
            e.embedding = $embedding,
            e.context_tags = $context_tags,
            e.metadata = $metadata
        ON MATCH SET 
            e.updated_at = datetime($updated_at),
            e.description = $description,
            e.canonical = $canonical,
            e.aliases = $aliases,
            e.embedding = $embedding,
            e.context_tags = $context_tags,
            e.metadata = $metadata
        RETURN e
        """

        params = self.to_dict()
        params["created_at"] = self.created_at.isoformat()
        params["updated_at"] = datetime.datetime.now().isoformat()

        # Convert metadata to JSON string
        params["metadata"] = json.dumps(params["metadata"])

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to save Entity {self.name}: {str(e)}")
            return False

    @classmethod
    def find_by_name(cls, db: Neo4jConnection, name: str) -> Optional["Entity"]:
        """
        Find an entity by name.

        Args:
            db: Neo4j connection
            name: Entity name

        Returns:
            Entity instance if found, None otherwise
        """
        query = "MATCH (e:Entity {name: $name}) RETURN e"
        try:
            result = db.execute_query_single(query, {"name": name})
            if result and "e" in result:
                return cls.from_dict(dict(result["e"]))
            return None
        except Exception as e:
            logger.error(f"Failed to find Entity {name}: {str(e)}")
            return None

    @classmethod
    def find_by_name_or_alias(
        cls, db: Neo4jConnection, name: str
    ) -> Optional["Entity"]:
        """
        Find an entity by name or alias.

        Args:
            db: Neo4j connection
            name: Entity name or alias

        Returns:
            Entity instance if found, None otherwise
        """
        query = """
        MATCH (e:Entity)
        WHERE e.name = $name OR $name IN e.aliases
        RETURN e
        """
        try:
            result = db.execute_query_single(query, {"name": name})
            if result and "e" in result:
                return cls.from_dict(dict(result["e"]))
            return None
        except Exception as e:
            logger.error(f"Failed to find Entity by name or alias {name}: {str(e)}")
            return None


@dataclass
class Event(Node):
    """
    Event node representing a temporal occurrence.
    """

    name: str = ""
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)
    description: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def save(self, db: Neo4jConnection) -> bool:
        """
        Save the event to the database.

        Args:
            db: Neo4j connection

        Returns:
            True if successful, False otherwise
        """
        query = """
        MERGE (e:Event {name: $name})
        ON CREATE SET 
            e.uid = $uid,
            e.created_at = datetime($created_at),
            e.timestamp = datetime($timestamp),
            e.description = $description,
            e.metadata = $metadata
        ON MATCH SET 
            e.updated_at = datetime($updated_at),
            e.timestamp = datetime($timestamp),
            e.description = $description,
            e.metadata = $metadata
        RETURN e
        """

        params = self.to_dict()
        params["created_at"] = self.created_at.isoformat()
        params["updated_at"] = datetime.datetime.now().isoformat()
        params["timestamp"] = self.timestamp.isoformat()

        # Convert metadata to JSON string
        params["metadata"] = json.dumps(params["metadata"])

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to save Event {self.name}: {str(e)}")
            return False


@dataclass
class Concept(Node):
    """
    Concept node representing an abstract idea or concept.
    """

    name: str = ""
    description: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def save(self, db: Neo4jConnection) -> bool:
        """
        Save the concept to the database.

        Args:
            db: Neo4j connection

        Returns:
            True if successful, False otherwise
        """
        query = """
        MERGE (c:Concept {name: $name})
        ON CREATE SET 
            c.uid = $uid,
            c.created_at = datetime($created_at),
            c.description = $description,
            c.metadata = $metadata
        ON MATCH SET 
            c.updated_at = datetime($updated_at),
            c.description = $description,
            c.metadata = $metadata
        RETURN c
        """

        params = self.to_dict()
        params["created_at"] = self.created_at.isoformat()
        params["updated_at"] = datetime.datetime.now().isoformat()

        # Convert metadata to JSON string
        params["metadata"] = json.dumps(params["metadata"])

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to save Concept {self.name}: {str(e)}")
            return False


@dataclass
class TimePeriod(Node):
    """
    TimePeriod node representing a specific time period for temporal validity of beliefs.
    """

    start_time: datetime.datetime = field(default_factory=datetime.datetime.now)
    end_time: Optional[datetime.datetime] = None
    description: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def save(self, db: Neo4jConnection) -> bool:
        """
        Save the time period to the database.

        Args:
            db: Neo4j connection

        Returns:
            True if successful, False otherwise
        """
        query = """
        CREATE (tp:TimePeriod)
        SET 
            tp.uid = $uid,
            tp.created_at = datetime($created_at),
            tp.start_time = datetime($start_time),
            tp.end_time = CASE WHEN $end_time IS NULL THEN NULL ELSE datetime($end_time) END,
            tp.description = $description,
            tp.metadata = $metadata
        RETURN tp
        """

        params = self.to_dict()
        params["created_at"] = self.created_at.isoformat()
        params["start_time"] = self.start_time.isoformat()
        params["end_time"] = self.end_time.isoformat() if self.end_time else None

        # Convert metadata to JSON string
        params["metadata"] = json.dumps(params["metadata"])

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to save TimePeriod: {str(e)}")
            return False


@dataclass
class SpeculationMarker(Node):
    """
    SpeculationMarker node indicating a belief is speculative and requires additional validation.
    """

    reason: str = ""  # Reason why the belief is marked as speculative
    validation_criteria: Optional[str] = None  # Criteria for validating the speculation
    metadata: Dict[str, Any] = field(default_factory=dict)

    def save(self, db: Neo4jConnection) -> bool:
        """
        Save the speculation marker to the database.

        Args:
            db: Neo4j connection

        Returns:
            True if successful, False otherwise
        """
        query = """
        CREATE (sm:SpeculationMarker)
        SET 
            sm.uid = $uid,
            sm.created_at = datetime($created_at),
            sm.reason = $reason,
            sm.validation_criteria = $validation_criteria,
            sm.metadata = $metadata
        RETURN sm
        """

        params = self.to_dict()
        params["created_at"] = self.created_at.isoformat()

        # Convert metadata to JSON string
        params["metadata"] = json.dumps(params["metadata"])

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to save SpeculationMarker: {str(e)}")
            return False


@dataclass
class TrustSnapshot(Node):
    """
    TrustSnapshot node tracking changes in a source's trust score over time.
    """

    score: float = 0.5  # Trust score at the time of snapshot
    at_time: datetime.datetime = field(
        default_factory=datetime.datetime.now
    )  # When the snapshot was taken
    source_id: str = ""  # ID of the source this snapshot belongs to
    metadata: Dict[str, Any] = field(default_factory=dict)

    def save(self, db: Neo4jConnection) -> bool:
        """
        Save the trust snapshot to the database.

        Args:
            db: Neo4j connection

        Returns:
            True if successful, False otherwise
        """
        query = """
        CREATE (ts:TrustSnapshot)
        SET 
            ts.uid = $uid,
            ts.created_at = datetime($created_at),
            ts.score = $score,
            ts.at_time = datetime($at_time),
            ts.source_id = $source_id,
            ts.metadata = $metadata
        RETURN ts
        """

        params = self.to_dict()
        params["created_at"] = self.created_at.isoformat()
        params["at_time"] = self.at_time.isoformat()

        # Convert metadata to JSON string
        params["metadata"] = json.dumps(params["metadata"])

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to save TrustSnapshot: {str(e)}")
            return False

    @classmethod
    def get_history_for_source(
        cls, db: Neo4jConnection, source_id: str
    ) -> List["TrustSnapshot"]:
        """
        Get the trust history for a specific source.

        Args:
            db: Neo4j connection
            source_id: ID of the source to get history for

        Returns:
            List of TrustSnapshot instances
        """
        query = """
        MATCH (ts:TrustSnapshot)
        WHERE ts.source_id = $source_id
        RETURN ts
        ORDER BY ts.at_time DESC
        """
        try:
            results = db.execute_query(query, {"source_id": source_id})
            return [cls.from_dict(dict(result["ts"])) for result in results]
        except Exception as e:
            logger.error(
                f"Failed to get trust history for source {source_id}: {str(e)}"
            )
            return []


@dataclass
class Source(Node):
    """
    Source node representing the origin of information.
    """

    name: str = ""
    type: SourceType = SourceType.USER
    trust_score: float = 0.5
    verification_status: str = "Pending"  # "Pending", "Verified", "Flagged"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def save(self, db: Neo4jConnection) -> bool:
        """
        Save the source to the database.

        Args:
            db: Neo4j connection

        Returns:
            True if successful, False otherwise
        """
        query = """
        MERGE (s:Source {name: $name})
        ON CREATE SET 
            s.uid = $uid,
            s.created_at = datetime($created_at),
            s.type = $type,
            s.trust_score = $trust_score,
            s.verification_status = $verification_status,
            s.metadata = $metadata
        ON MATCH SET 
            s.updated_at = datetime($updated_at),
            s.type = $type,
            s.trust_score = $trust_score,
            s.verification_status = $verification_status,
            s.metadata = $metadata
        RETURN s
        """

        params = self.to_dict()
        params["created_at"] = self.created_at.isoformat()
        params["updated_at"] = datetime.datetime.now().isoformat()
        params["type"] = self.type.value

        # Convert metadata to JSON string
        params["metadata"] = json.dumps(params["metadata"])

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to save Source {self.name}: {str(e)}")
            return False

    def record_trust_snapshot(self, db: Neo4jConnection) -> Optional[TrustSnapshot]:
        """
        Record a snapshot of the current trust score.

        Args:
            db: Neo4j connection

        Returns:
            TrustSnapshot instance if successful, None otherwise
        """
        snapshot = TrustSnapshot(
            score=self.trust_score, at_time=datetime.datetime.now(), source_id=self.uid
        )

        if snapshot.save(db):
            # Create the relationship
            query = """
            MATCH (s:Source {uid: $source_uid})
            MATCH (ts:TrustSnapshot {uid: $snapshot_uid})
            MERGE (s)-[r:HAD_TRUST]->(ts)
            SET r.score = $score,
                r.at_time = datetime($at_time),
                r.created_at = datetime($created_at)
            RETURN r
            """

            params = {
                "source_uid": self.uid,
                "snapshot_uid": snapshot.uid,
                "score": snapshot.score,
                "at_time": snapshot.at_time.isoformat(),
                "created_at": datetime.datetime.now().isoformat(),
            }

            try:
                db.execute_write_transaction(query, params)
                return snapshot
            except Exception as e:
                logger.error(f"Failed to create HAD_TRUST relationship: {str(e)}")
                return None

        return None

    def report_event(self, db: Neo4jConnection, event: Event) -> bool:
        """
        Mark this source as having reported an event.

        Args:
            db: Neo4j connection
            event: Event node

        Returns:
            True if successful, False otherwise
        """
        query = """
        MATCH (s:Source {name: $source_name})
        MATCH (e:Event {name: $event_name})
        MERGE (s)-[r:REPORTED]->(e)
        ON CREATE SET r.created_at = datetime($created_at)
        ON MATCH SET r.updated_at = datetime($updated_at)
        RETURN r
        """

        params = {
            "source_name": self.name,
            "event_name": event.name,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
        }

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to mark source as reporting event: {str(e)}")
            return False


@dataclass
class Belief(Node):
    """
    Belief node representing a statement with a confidence score.
    """

    statement: str = ""
    confidence: float = 0.5
    last_updated: datetime.datetime = field(default_factory=datetime.datetime.now)
    expires_at: Optional[datetime.datetime] = None  # Optional expiration date
    version: int = 1  # Versioning for belief tracking
    category: str = ""  # Category label (e.g., "Science", "Politics")
    speculative: bool = (
        False  # Whether this belief is based on speculation or uncertainty
    )
    metadata: Dict[str, Any] = field(default_factory=dict)

    def save(self, db: Neo4jConnection) -> bool:
        """
        Save the belief to the database.

        Args:
            db: Neo4j connection

        Returns:
            True if successful, False otherwise
        """
        query = """
        MERGE (b:Belief {statement: $statement})
        ON CREATE SET 
            b.uid = $uid,
            b.created_at = datetime($created_at),
            b.confidence = $confidence,
            b.last_updated = datetime($last_updated),
            b.expires_at = CASE WHEN $expires_at IS NULL THEN NULL ELSE datetime($expires_at) END,
            b.version = $version,
            b.category = $category,
            b.speculative = $speculative,
            b.metadata = $metadata
        ON MATCH SET 
            b.updated_at = datetime($updated_at),
            b.confidence = $confidence,
            b.last_updated = datetime($last_updated),
            b.expires_at = CASE WHEN $expires_at IS NULL THEN NULL ELSE datetime($expires_at) END,
            b.version = $version,
            b.category = $category,
            b.speculative = $speculative,
            b.metadata = $metadata
        RETURN b
        """

        params = self.to_dict()
        params["created_at"] = self.created_at.isoformat()
        params["updated_at"] = datetime.datetime.now().isoformat()
        params["last_updated"] = self.last_updated.isoformat()
        params["expires_at"] = self.expires_at.isoformat() if self.expires_at else None
        params["version"] = self.version
        params["category"] = self.category
        params["speculative"] = self.speculative

        # Convert metadata to JSON string
        params["metadata"] = json.dumps(params["metadata"])

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to save Belief {self.statement}: {str(e)}")
            return False

    def link_to_source(
        self,
        db: Neo4jConnection,
        source: Source,
        relationship_type: str = "SUPPORTED_BY",
    ) -> bool:
        """
        Link this belief to a source.

        Args:
            db: Neo4j connection
            source: Source node
            relationship_type: Type of relationship (SUPPORTED_BY or CONTRADICTED_BY)

        Returns:
            True if successful, False otherwise
        """
        if relationship_type not in ["SUPPORTED_BY", "CONTRADICTED_BY"]:
            raise ValueError(
                "relationship_type must be either SUPPORTED_BY or CONTRADICTED_BY"
            )

        query = f"""
        MATCH (b:Belief {{statement: $statement}})
        MATCH (s:Source {{name: $source_name}})
        MERGE (b)-[r:{relationship_type}]->(s)
        ON CREATE SET r.created_at = datetime($created_at)
        ON MATCH SET r.updated_at = datetime($updated_at)
        RETURN r
        """

        params = {
            "statement": self.statement,
            "source_name": source.name,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
        }

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to link Belief to Source: {str(e)}")
            return False

    def link_to_entity(self, db: Neo4jConnection, entity: Entity) -> bool:
        """
        Link this belief to an entity.

        Args:
            db: Neo4j connection
            entity: Entity node

        Returns:
            True if successful, False otherwise
        """
        query = """
        MATCH (b:Belief {statement: $statement})
        MATCH (e:Entity {name: $entity_name})
        MERGE (e)-[r:BELIEVES]->(b)
        ON CREATE SET r.created_at = datetime($created_at)
        ON MATCH SET r.updated_at = datetime($updated_at)
        RETURN r
        """

        params = {
            "statement": self.statement,
            "entity_name": entity.name,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
        }

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to link Belief to Entity: {str(e)}")
            return False

    def link_to_event(self, db: Neo4jConnection, event: Event) -> bool:
        """
        Link this belief to an event that shaped it.

        Args:
            db: Neo4j connection
            event: Event node

        Returns:
            True if successful, False otherwise
        """
        query = """
        MATCH (b:Belief {statement: $statement})
        MATCH (e:Event {name: $event_name})
        MERGE (b)-[r:SHAPED_BY]->(e)
        ON CREATE SET r.created_at = datetime($created_at)
        ON MATCH SET r.updated_at = datetime($updated_at)
        RETURN r
        """

        params = {
            "statement": self.statement,
            "event_name": event.name,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
        }

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to link Belief to Event: {str(e)}")
            return False

    def mark_contradiction(
        self, db: Neo4jConnection, contradicting_belief: "Belief"
    ) -> bool:
        """
        Mark this belief as contradicting another belief.

        Args:
            db: Neo4j connection
            contradicting_belief: The belief that contradicts this one

        Returns:
            True if successful, False otherwise
        """
        query = """
        MATCH (b1:Belief {statement: $statement1})
        MATCH (b2:Belief {statement: $statement2})
        MERGE (b1)-[r:CONTRADICTS]->(b2)
        ON CREATE SET r.created_at = datetime($created_at)
        ON MATCH SET r.updated_at = datetime($updated_at)
        RETURN r
        """

        params = {
            "statement1": self.statement,
            "statement2": contradicting_belief.statement,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
        }

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to mark contradiction between beliefs: {str(e)}")
            return False

    def mark_as_speculative(
        self, db: Neo4jConnection, marker: SpeculationMarker
    ) -> bool:
        """
        Mark this belief as speculative.

        Args:
            db: Neo4j connection
            marker: SpeculationMarker node

        Returns:
            True if successful, False otherwise
        """
        query = """
        MATCH (b:Belief {statement: $statement})
        MATCH (sm:SpeculationMarker {uid: $marker_uid})
        MERGE (b)-[r:MARKED_SPECULATIVE]->(sm)
        ON CREATE SET r.created_at = datetime($created_at)
        ON MATCH SET r.updated_at = datetime($updated_at)
        RETURN r
        """

        params = {
            "statement": self.statement,
            "marker_uid": marker.uid,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
        }

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to mark belief as speculative: {str(e)}")
            return False

    def set_valid_time_period(
        self, db: Neo4jConnection, time_period: TimePeriod
    ) -> bool:
        """
        Set the time period during which this belief is valid.

        Args:
            db: Neo4j connection
            time_period: TimePeriod node

        Returns:
            True if successful, False otherwise
        """
        query = """
        MATCH (b:Belief {statement: $statement})
        MATCH (tp:TimePeriod {uid: $time_period_uid})
        MERGE (b)-[r:VALID_DURING]->(tp)
        SET r.start_time = datetime($start_time),
            r.end_time = CASE WHEN $end_time IS NULL THEN NULL ELSE datetime($end_time) END,
            r.created_at = CASE WHEN r.created_at IS NULL THEN datetime($created_at) ELSE r.created_at END,
            r.updated_at = datetime($updated_at)
        RETURN r
        """

        params = {
            "statement": self.statement,
            "time_period_uid": time_period.uid,
            "start_time": time_period.start_time.isoformat(),
            "end_time": (
                time_period.end_time.isoformat() if time_period.end_time else None
            ),
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
        }

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to set valid time period for belief: {str(e)}")
            return False


@dataclass
class Opinion(Node):
    """
    Opinion node representing a synthesized opinion from multiple beliefs.
    """

    statement: str = ""
    confidence: float = 0.5
    stance: OpinionStance = OpinionStance.NEUTRAL
    clarity: float = 0.5
    time_horizon: TimeHorizon = TimeHorizon.SHORT_TERM
    resistance_factor: float = 0.8
    version: int = 1  # Add version tracking
    updated_by: str = "system"  # Track what updated this opinion
    last_updated: datetime.datetime = field(
        default_factory=datetime.datetime.now
    )  # Last modified timestamp
    update_history: List[Dict[str, Any]] = field(
        default_factory=list
    )  # Track update history
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Opinion":
        """
        Create an Opinion instance from a dictionary.

        Args:
            data: Dictionary containing opinion data

        Returns:
            Opinion instance
        """
        # Convert time_horizon string to enum if needed
        if "time_horizon" in data:
            if isinstance(data["time_horizon"], str):
                data["time_horizon"] = TimeHorizon.from_string(data["time_horizon"])

        # Convert stance string to enum if needed
        if "stance" in data:
            if isinstance(data["stance"], str):
                try:
                    data["stance"] = OpinionStance(data["stance"])
                except ValueError:
                    # Default to NEUTRAL if invalid value
                    data["stance"] = OpinionStance.NEUTRAL

        # Parse metadata if it's a JSON string
        if "metadata" in data and isinstance(data["metadata"], str):
            try:
                data["metadata"] = json.loads(data["metadata"])
            except json.JSONDecodeError:
                data["metadata"] = {}

        # Convert timestamps to datetime objects
        for ts_field in ["last_updated", "created_at", "updated_at"]:
            if ts_field in data and isinstance(data[ts_field], str):
                try:
                    data[ts_field] = datetime.datetime.fromisoformat(
                        data[ts_field].replace("Z", "+00:00")
                    )
                except ValueError:
                    data[ts_field] = datetime.datetime.now()

        # Create instance with cleaned data
        return cls(
            **{k: v for k, v in data.items() if k in inspect.signature(cls).parameters}
        )

    def save(self, db: Neo4jConnection) -> bool:
        """
        Save the opinion to the database.

        Args:
            db: Neo4j connection

        Returns:
            True if successful, False otherwise
        """
        query = """
        MERGE (o:Opinion {statement: $statement})
        ON CREATE SET 
            o.uid = $uid,
            o.created_at = datetime($created_at),
            o.confidence = $confidence,
            o.stance = $stance,
            o.clarity = $clarity,
            o.time_horizon = $time_horizon,
            o.resistance_factor = $resistance_factor,
            o.version = $version,
            o.updated_by = $updated_by,
            o.last_updated = datetime($last_updated),
            o.update_history = $update_history,
            o.metadata = $metadata
        ON MATCH SET 
            o.updated_at = datetime($updated_at),
            o.confidence = $confidence,
            o.stance = $stance,
            o.clarity = $clarity,
            o.time_horizon = $time_horizon,
            o.resistance_factor = $resistance_factor,
            o.version = $version,
            o.updated_by = $updated_by,
            o.last_updated = datetime($last_updated),
            o.update_history = $update_history,
            o.metadata = $metadata
        RETURN o
        """

        params = self.to_dict()
        params["created_at"] = self.created_at.isoformat()
        params["updated_at"] = datetime.datetime.now().isoformat()
        params["stance"] = self.stance.value
        params["time_horizon"] = self.time_horizon.value

        # Convert metadata to JSON string
        params["metadata"] = json.dumps(params["metadata"])

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to save Opinion {self.statement}: {str(e)}")
            return False

    def create_audit_record(
        self, db: Neo4jConnection, previous_version: Optional["Opinion"] = None
    ) -> bool:
        """
        Create an audit record for this opinion update.

        Args:
            db: Neo4j connection
            previous_version: Previous version of the opinion, if any

        Returns:
            True if successful, False otherwise
        """
        if previous_version is None:
            # This is a new opinion, create initial audit record
            query = """
            MATCH (o:Opinion {uid: $opinion_uid})
            CREATE (a:AuditRecord {
                uid: $audit_uid,
                created_at: datetime($created_at),
                action: 'CREATE',
                opinion_uid: $opinion_uid,
                opinion_statement: $statement,
                confidence: $confidence,
                stance: $stance,
                version: $version,
                updated_by: $updated_by
            })
            CREATE (o)-[:HAS_AUDIT]->(a)
            RETURN a
            """

            params = {
                "audit_uid": str(uuid4()),
                "created_at": datetime.datetime.now().isoformat(),
                "opinion_uid": self.uid,
                "statement": self.statement,
                "confidence": self.confidence,
                "stance": (
                    self.stance.value
                    if isinstance(self.stance, OpinionStance)
                    else self.stance
                ),
                "version": self.version,
                "updated_by": self.updated_by,
            }
        else:
            # This is an update, create update audit record
            query = """
            MATCH (o:Opinion {uid: $opinion_uid})
            CREATE (a:AuditRecord {
                uid: $audit_uid,
                created_at: datetime($created_at),
                action: 'UPDATE',
                opinion_uid: $opinion_uid,
                opinion_statement: $statement,
                previous_confidence: $previous_confidence,
                new_confidence: $new_confidence,
                previous_stance: $previous_stance,
                new_stance: $new_stance,
                previous_version: $previous_version,
                new_version: $new_version,
                updated_by: $updated_by
            })
            CREATE (o)-[:HAS_AUDIT]->(a)
            RETURN a
            """

            params = {
                "audit_uid": str(uuid4()),
                "created_at": datetime.datetime.now().isoformat(),
                "opinion_uid": self.uid,
                "statement": self.statement,
                "previous_confidence": previous_version.confidence,
                "new_confidence": self.confidence,
                "previous_stance": (
                    previous_version.stance.value
                    if isinstance(previous_version.stance, OpinionStance)
                    else previous_version.stance
                ),
                "new_stance": (
                    self.stance.value
                    if isinstance(self.stance, OpinionStance)
                    else self.stance
                ),
                "previous_version": previous_version.version,
                "new_version": self.version,
                "updated_by": self.updated_by,
            }

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(
                f"Failed to create audit record for Opinion {self.statement}: {str(e)}"
            )
            return False

    def link_to_belief(self, db: Neo4jConnection, belief: Belief) -> bool:
        """
        Link this opinion to a belief.

        Args:
            db: Neo4j connection
            belief: Belief node

        Returns:
            True if successful, False otherwise
        """
        query = """
        MATCH (o:Opinion {statement: $opinion_statement})
        MATCH (b:Belief {statement: $belief_statement})
        MERGE (o)-[r:SYNTHESIZED_FROM]->(b)
        ON CREATE SET r.created_at = datetime($created_at)
        ON MATCH SET r.updated_at = datetime($updated_at)
        RETURN r
        """

        params = {
            "opinion_statement": self.statement,
            "belief_statement": belief.statement,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
        }

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to link Opinion to Belief: {str(e)}")
            return False

    def link_to_concept(self, db: Neo4jConnection, concept: Concept) -> bool:
        """
        Link this opinion to a concept.

        Args:
            db: Neo4j connection
            concept: Concept node

        Returns:
            True if successful, False otherwise
        """
        query = """
        MATCH (o:Opinion {statement: $opinion_statement})
        MATCH (c:Concept {name: $concept_name})
        MERGE (o)-[r:BASED_ON]->(c)
        ON CREATE SET r.created_at = datetime($created_at)
        ON MATCH SET r.updated_at = datetime($updated_at)
        RETURN r
        """

        params = {
            "opinion_statement": self.statement,
            "concept_name": concept.name,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
        }

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to link Opinion to Concept: {str(e)}")
            return False

    def link_to_event(self, db: Neo4jConnection, event: Event) -> bool:
        """
        Link this opinion to an event.

        Args:
            db: Neo4j connection
            event: Event node

        Returns:
            True if successful, False otherwise
        """
        query = """
        MATCH (o:Opinion {statement: $opinion_statement})
        MATCH (e:Event {name: $event_name})
        MERGE (o)-[r:BASED_ON]->(e)
        ON CREATE SET r.created_at = datetime($created_at)
        ON MATCH SET r.updated_at = datetime($updated_at)
        RETURN r
        """

        params = {
            "opinion_statement": self.statement,
            "event_name": event.name,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
        }

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to link Opinion to Event: {str(e)}")
            return False

    def set_resistance_factor(
        self, db: Neo4jConnection, target_opinion: "Opinion", score: float
    ) -> bool:
        """
        Set the resistance factor between this opinion and another.

        Args:
            db: Neo4j connection
            target_opinion: Target Opinion node
            score: Resistance factor score (0.0 to 1.0)

        Returns:
            True if successful, False otherwise
        """
        query = """
        MATCH (o1:Opinion {statement: $opinion1_statement})
        MATCH (o2:Opinion {statement: $opinion2_statement})
        MERGE (o1)-[r:HAS_RESISTANCE_FACTOR]->(o2)
        SET r.score = $score,
            r.created_at = CASE WHEN r.created_at IS NULL THEN datetime($created_at) ELSE r.created_at END,
            r.updated_at = datetime($updated_at)
        RETURN r
        """

        params = {
            "opinion1_statement": self.statement,
            "opinion2_statement": target_opinion.statement,
            "score": score,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
        }

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to set resistance factor between opinions: {str(e)}")
            return False

    def replace_opinion(self, db: Neo4jConnection, old_opinion: "Opinion") -> bool:
        """
        Mark this opinion as replacing an older opinion.

        Args:
            db: Neo4j connection
            old_opinion: The opinion being replaced

        Returns:
            True if successful, False otherwise
        """
        query = """
        MATCH (new:Opinion {statement: $new_statement})
        MATCH (old:Opinion {statement: $old_statement})
        MERGE (new)-[r:REPLACES]->(old)
        ON CREATE SET r.created_at = datetime($created_at)
        ON MATCH SET r.updated_at = datetime($updated_at)
        RETURN r
        """

        params = {
            "new_statement": self.statement,
            "old_statement": old_opinion.statement,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
        }

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to mark opinion replacement: {str(e)}")
            return False


@dataclass
class OpinionSummary(Node):
    """
    OpinionSummary node storing high-level summaries of opinions.
    """

    statement: str = ""  # Condensed version of the opinion
    confidence: float = 0.5  # Aggregate confidence score
    linked_opinion_ids: List[str] = field(
        default_factory=list
    )  # Referenced opinion nodes
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def save(self, db: Neo4jConnection) -> bool:
        """
        Save the opinion summary to the database.

        Args:
            db: Neo4j connection

        Returns:
            True if successful, False otherwise
        """
        query = """
        MERGE (os:OpinionSummary {statement: $statement})
        ON CREATE SET 
            os.uid = $uid,
            os.created_at = datetime($created_at),
            os.confidence = $confidence,
            os.linked_opinion_ids = $linked_opinion_ids,
            os.metadata = $metadata
        ON MATCH SET 
            os.updated_at = datetime($updated_at),
            os.confidence = $confidence,
            os.linked_opinion_ids = $linked_opinion_ids,
            os.metadata = $metadata
        RETURN os
        """

        params = self.to_dict()
        params["created_at"] = self.created_at.isoformat()
        params["updated_at"] = datetime.datetime.now().isoformat()

        # Convert metadata to JSON string
        params["metadata"] = json.dumps(params["metadata"])

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to save OpinionSummary {self.statement}: {str(e)}")
            return False

    def link_to_opinion(self, db: Neo4jConnection, opinion: Opinion) -> bool:
        """
        Link this opinion summary to an opinion.

        Args:
            db: Neo4j connection
            opinion: Opinion node

        Returns:
            True if successful, False otherwise
        """
        query = """
        MATCH (os:OpinionSummary {statement: $summary_statement})
        MATCH (o:Opinion {statement: $opinion_statement})
        MERGE (o)-[r:EXPANDED_IN_DETAIL]->(os)
        ON CREATE SET r.created_at = datetime($created_at)
        ON MATCH SET r.updated_at = datetime($updated_at)
        RETURN r
        """

        params = {
            "summary_statement": self.statement,
            "opinion_statement": opinion.statement,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
        }

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to link Opinion to OpinionSummary: {str(e)}")
            return False


@dataclass
class BalanceAudit(Node):
    """
    BalanceAudit node tracking bias and opinion polarization within the graph.
    """

    last_run: datetime.datetime = field(default_factory=datetime.datetime.now)
    skewness_score: float = 0.0  # How skewed opinions are
    recommended_action: Optional[str] = None  # Suggested bias correction action
    metadata: Dict[str, Any] = field(default_factory=dict)

    def save(self, db: Neo4jConnection) -> bool:
        """
        Save the balance audit to the database.

        Args:
            db: Neo4j connection

        Returns:
            True if successful, False otherwise
        """
        query = """
        CREATE (ba:BalanceAudit)
        SET 
            ba.uid = $uid,
            ba.created_at = datetime($created_at),
            ba.last_run = datetime($last_run),
            ba.skewness_score = $skewness_score,
            ba.recommended_action = $recommended_action,
            ba.metadata = $metadata
        RETURN ba
        """

        params = self.to_dict()
        params["created_at"] = self.created_at.isoformat()
        params["last_run"] = self.last_run.isoformat()

        # Convert metadata to JSON string
        params["metadata"] = json.dumps(params["metadata"])

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to save BalanceAudit: {str(e)}")
            return False

    @classmethod
    def get_latest(cls, db: Neo4jConnection) -> Optional["BalanceAudit"]:
        """
        Get the latest balance audit.

        Args:
            db: Neo4j connection

        Returns:
            BalanceAudit instance if found, None otherwise
        """
        query = """
        MATCH (ba:BalanceAudit)
        RETURN ba
        ORDER BY ba.last_run DESC
        LIMIT 1
        """
        try:
            result = db.execute_query_single(query, {})
            if result and "ba" in result:
                return cls.from_dict(dict(result["ba"]))
            return None
        except Exception as e:
            logger.error(f"Failed to get latest BalanceAudit: {str(e)}")
            return None


@dataclass
class AuditRecord(Node):
    """
    AuditRecord node tracking historical opinion changes and belief updates.
    """

    action: str = ""  # Type of action (e.g., "CREATE", "UPDATE")
    node_type: str = ""  # Type of node being audited
    node_id: str = ""  # ID of the node being audited
    previous_confidence: Optional[float] = None  # Previous confidence score
    new_confidence: Optional[float] = None  # New confidence score
    previous_version: Optional[int] = None  # Previous version number
    new_version: Optional[int] = None  # New version number
    updated_by: str = ""  # Entity that performed the update
    reason: Optional[str] = None  # Reason for the update
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def save(self, db: Neo4jConnection) -> bool:
        """
        Save the audit record to the database.

        Args:
            db: Neo4j connection

        Returns:
            True if successful, False otherwise
        """
        query = """
        CREATE (ar:AuditRecord)
        SET 
            ar.uid = $uid,
            ar.created_at = datetime($created_at),
            ar.action = $action,
            ar.node_type = $node_type,
            ar.node_id = $node_id,
            ar.previous_confidence = $previous_confidence,
            ar.new_confidence = $new_confidence,
            ar.previous_version = $previous_version,
            ar.new_version = $new_version,
            ar.updated_by = $updated_by,
            ar.reason = $reason,
            ar.timestamp = datetime($timestamp),
            ar.metadata = $metadata
        RETURN ar
        """

        params = self.to_dict()
        params["created_at"] = self.created_at.isoformat()
        params["timestamp"] = self.timestamp.isoformat()

        # Convert metadata to JSON string
        params["metadata"] = json.dumps(params["metadata"])

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to save AuditRecord: {str(e)}")
            return False

    @classmethod
    def get_history_for_node(
        cls, db: Neo4jConnection, node_id: str
    ) -> List["AuditRecord"]:
        """
        Get the audit history for a specific node.

        Args:
            db: Neo4j connection
            node_id: ID of the node to get history for

        Returns:
            List of AuditRecord instances
        """
        query = """
        MATCH (ar:AuditRecord)
        WHERE ar.node_id = $node_id
        RETURN ar
        ORDER BY ar.timestamp DESC
        """
        try:
            results = db.execute_query(query, {"node_id": node_id})
            return [cls.from_dict(dict(result["ar"])) for result in results]
        except Exception as e:
            logger.error(f"Failed to get audit history for node {node_id}: {str(e)}")
            return []


@dataclass
class ConflictResolution(Node):
    """
    ConflictResolution node for handling contradictions in the knowledge graph.
    """

    topic: str = ""
    status: ConflictStatus = ConflictStatus.ACTIVE
    description: Optional[str] = None
    resolution_details: Optional[str] = None  # Description of resolution outcome
    resolved_by: Optional[str] = None  # Who resolved it
    resolved_at: Optional[datetime.datetime] = None  # Timestamp of resolution
    priority: float = 0.5  # Urgency of resolution (0.0 to 1.0)
    temporal_window: Dict[str, Any] = field(
        default_factory=dict
    )  # Defines valid time ranges for conflicting beliefs
    metadata: Dict[str, Any] = field(default_factory=dict)

    def save(self, db: Neo4jConnection) -> bool:
        """
        Save the conflict resolution to the database.

        Args:
            db: Neo4j connection

        Returns:
            True if successful, False otherwise
        """
        query = """
        MERGE (cr:ConflictResolution {topic: $topic})
        ON CREATE SET 
            cr.uid = $uid,
            cr.created_at = datetime($created_at),
            cr.status = $status,
            cr.description = $description,
            cr.resolution_details = $resolution_details,
            cr.resolved_by = $resolved_by,
            cr.resolved_at = CASE WHEN $resolved_at IS NULL THEN NULL ELSE datetime($resolved_at) END,
            cr.priority = $priority,
            cr.temporal_window = $temporal_window,
            cr.metadata = $metadata
        ON MATCH SET 
            cr.updated_at = datetime($updated_at),
            cr.status = $status,
            cr.description = $description,
            cr.resolution_details = $resolution_details,
            cr.resolved_by = $resolved_by,
            cr.resolved_at = CASE WHEN $resolved_at IS NULL THEN NULL ELSE datetime($resolved_at) END,
            cr.priority = $priority,
            cr.temporal_window = $temporal_window,
            cr.metadata = $metadata
        RETURN cr
        """

        params = self.to_dict()
        params["created_at"] = self.created_at.isoformat()
        params["updated_at"] = datetime.datetime.now().isoformat()
        params["status"] = self.status.value
        params["resolution_details"] = self.resolution_details
        params["resolved_by"] = self.resolved_by
        params["resolved_at"] = (
            self.resolved_at.isoformat() if self.resolved_at else None
        )
        params["priority"] = self.priority
        params["temporal_window"] = json.dumps(self.temporal_window)

        # Convert metadata to JSON string
        params["metadata"] = json.dumps(params["metadata"])

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to save ConflictResolution {self.topic}: {str(e)}")
            return False

    def link_to_belief(self, db: Neo4jConnection, belief: Belief) -> bool:
        """
        Link this conflict resolution to a belief.

        Args:
            db: Neo4j connection
            belief: Belief node

        Returns:
            True if successful, False otherwise
        """
        query = """
        MATCH (cr:ConflictResolution {topic: $topic})
        MATCH (b:Belief {statement: $statement})
        MERGE (cr)-[r:INVOLVES]->(b)
        ON CREATE SET r.created_at = datetime($created_at)
        ON MATCH SET r.updated_at = datetime($updated_at)
        RETURN r
        """

        params = {
            "topic": self.topic,
            "statement": belief.statement,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
        }

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to link ConflictResolution to Belief: {str(e)}")
            return False

    def set_temporal_bound(self, db: Neo4jConnection, belief: Belief) -> bool:
        """
        Set a temporal bound for a belief in this conflict resolution.

        Args:
            db: Neo4j connection
            belief: Belief node

        Returns:
            True if successful, False otherwise
        """
        query = """
        MATCH (cr:ConflictResolution {topic: $topic})
        MATCH (b:Belief {statement: $statement})
        MERGE (cr)-[r:TEMPORALLY_BOUND]->(b)
        ON CREATE SET r.created_at = datetime($created_at)
        ON MATCH SET r.updated_at = datetime($updated_at)
        RETURN r
        """

        params = {
            "topic": self.topic,
            "statement": belief.statement,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
        }

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to set temporal bound for belief: {str(e)}")
            return False


@dataclass
class DecisionContext(Node):
    """
    DecisionContext node representing contextual constraints for opinions and beliefs.
    """

    name: str = ""
    priority: List[str] = field(
        default_factory=list
    )  # Ranked list of influencing factors
    metadata: Dict[str, Any] = field(default_factory=dict)

    def save(self, db: Neo4jConnection) -> bool:
        """
        Save the decision context to the database.

        Args:
            db: Neo4j connection

        Returns:
            True if successful, False otherwise
        """
        query = """
        MERGE (dc:DecisionContext {name: $name})
        ON CREATE SET 
            dc.uid = $uid,
            dc.created_at = datetime($created_at),
            dc.priority = $priority,
            dc.metadata = $metadata
        ON MATCH SET 
            dc.updated_at = datetime($updated_at),
            dc.priority = $priority,
            dc.metadata = $metadata
        RETURN dc
        """

        params = self.to_dict()
        params["created_at"] = self.created_at.isoformat()
        params["updated_at"] = datetime.datetime.now().isoformat()

        # Convert metadata to JSON string
        params["metadata"] = json.dumps(params["metadata"])

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to save DecisionContext {self.name}: {str(e)}")
            return False

    def apply_to_opinion(self, db: Neo4jConnection, opinion: Opinion) -> bool:
        """
        Apply this decision context to an opinion.

        Args:
            db: Neo4j connection
            opinion: Opinion node

        Returns:
            True if successful, False otherwise
        """
        query = """
        MATCH (dc:DecisionContext {name: $context_name})
        MATCH (o:Opinion {statement: $opinion_statement})
        MERGE (dc)-[r:APPLIES_TO]->(o)
        ON CREATE SET r.created_at = datetime($created_at)
        ON MATCH SET r.updated_at = datetime($updated_at)
        RETURN r
        """

        params = {
            "context_name": self.name,
            "opinion_statement": opinion.statement,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
        }

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to apply DecisionContext to Opinion: {str(e)}")
            return False

    def apply_to_belief(self, db: Neo4jConnection, belief: Belief) -> bool:
        """
        Apply this decision context to a belief.

        Args:
            db: Neo4j connection
            belief: Belief node

        Returns:
            True if successful, False otherwise
        """
        query = """
        MATCH (dc:DecisionContext {name: $context_name})
        MATCH (b:Belief {statement: $belief_statement})
        MERGE (dc)-[r:APPLIES_TO]->(b)
        ON CREATE SET r.created_at = datetime($created_at)
        ON MATCH SET r.updated_at = datetime($updated_at)
        RETURN r
        """

        params = {
            "context_name": self.name,
            "belief_statement": belief.statement,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
        }

        try:
            return db.execute_write_transaction(query, params)
        except Exception as e:
            logger.error(f"Failed to apply DecisionContext to Belief: {str(e)}")
            return False
