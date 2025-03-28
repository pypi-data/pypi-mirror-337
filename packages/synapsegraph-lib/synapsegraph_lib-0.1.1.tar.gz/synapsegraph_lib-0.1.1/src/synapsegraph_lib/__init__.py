"""
SynapseGraph - A graph-based AI system for dynamic knowledge representation with temporal awareness.

This package provides tools for modeling beliefs, opinions, and their relationships
while automatically handling confidence decay, conflict resolution, and uncertainty.
"""

__version__ = "0.1.1"

# Import main components for easier importing by users
from synapsegraph_lib.core.database import Neo4jConnection
from synapsegraph_lib.core.synapse_graph import SynapseGraph
from synapsegraph_lib.ingestion.ingestor import (
    UserInputIngestor,
    FileIngestor,
    WebContentIngestor,
    ResearchIngestor,
    APIIngestor,
    BatchIngestor,
)
from synapsegraph_lib.integrity.balance_monitoring import BalanceMonitor

# Export key models
from synapsegraph_lib.core.models import Entity, Belief, Opinion, Source

# Export enums from config
from synapsegraph_lib.core.config import SourceType, OpinionStance, TimeHorizon


# Convenience function to create and initialize a SynapseGraph instance
def create_synapse_graph(uri=None, username=None, password=None, database=None):
    """
    Create and initialize a SynapseGraph instance with a Neo4j connection.

    If connection parameters are not provided, they will be loaded from
    environment variables or default configuration.

    Args:
        uri: Neo4j URI (default: from environment variable NEO4J_URI)
        username: Neo4j username (default: from environment variable NEO4J_USERNAME)
        password: Neo4j password (default: from environment variable NEO4J_PASSWORD)
        database: Neo4j database name (default: from environment variable NEO4J_DATABASE)

    Returns:
        Initialized SynapseGraph instance
    """
    from synapsegraph_lib.core.config import config

    # Use provided parameters or defaults from config
    uri = uri or config.database.uri
    username = username or config.database.username
    password = password or config.database.password
    database = database or config.database.database

    # Create database connection
    db = Neo4jConnection(
        uri=uri, username=username, password=password, database=database
    )

    # Initialize and return SynapseGraph
    return SynapseGraph(db)
