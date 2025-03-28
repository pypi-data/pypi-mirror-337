"""
Database connection module for Neo4j integration.

This module provides a singleton connection to the Neo4j database and
utility functions for common database operations.
"""

import os
import logging
from typing import Dict, List, Optional, Any, Union
from neo4j import GraphDatabase, Driver, Session, Result

logger = logging.getLogger(__name__)


class Neo4jConnection:
    """
    Singleton class for managing Neo4j database connections.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Neo4jConnection, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(
        self, config=None, uri: str = None, username: str = None, password: str = None
    ):
        """
        Initialize the Neo4j connection.

        Args:
            config: DatabaseConfig object containing connection details
            uri: Neo4j connection URI (defaults to environment variable NEO4J_URI)
            username: Neo4j username (defaults to environment variable NEO4J_USERNAME)
            password: Neo4j password (defaults to environment variable NEO4J_PASSWORD)
        """
        if self._initialized:
            return

        # If a config object is provided, use it
        if config is not None:
            self.uri = config.uri
            self.username = config.username
            self.password = config.password
            self.database = getattr(config, "database", None)
        else:
            # Otherwise use the individual parameters or environment variables
            self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
            self.username = username or os.getenv("NEO4J_USERNAME", "neo4j")
            self.password = password or os.getenv("NEO4J_PASSWORD", "password")
            self.database = os.getenv("NEO4J_DATABASE", None)

        self._driver = None
        self._initialized = True

    @property
    def driver(self) -> Driver:
        """
        Get the Neo4j driver instance, creating it if it doesn't exist.

        Returns:
            Neo4j driver instance
        """
        if self._driver is None:
            try:
                self._driver = GraphDatabase.driver(
                    self.uri, auth=(self.username, self.password)
                )
                logger.info(f"Connected to Neo4j database at {self.uri}")
            except Exception as e:
                logger.error(f"Failed to connect to Neo4j: {str(e)}")
                raise
        return self._driver

    def close(self):
        """Close the Neo4j driver connection."""
        if self._driver is not None:
            self._driver.close()
            self._driver = None
            logger.info("Neo4j connection closed")

    def verify_connection(self) -> bool:
        """
        Verify that the connection to Neo4j is working.

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            with self.driver.session() as session:
                result = session.run("RETURN 1 AS test")
                record = result.single()
                return record and record["test"] == 1
        except Exception as e:
            logger.error(f"Connection verification failed: {str(e)}")
            return False

    def execute_query(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None,
        database: Optional[str] = None,
        fetch_all: bool = False,
    ) -> Union[Result, List[Dict[str, Any]]]:
        """
        Execute a Cypher query and return the result.

        Args:
            query: Cypher query string
            parameters: Query parameters
            database: Database name (optional)
            fetch_all: Whether to fetch all results as a list of dictionaries

        Returns:
            Query result or list of dictionaries
        """
        try:
            with self.get_session(database) as session:
                result = session.run(query, parameters or {})
                if fetch_all:
                    return [dict(record) for record in result]
                return result
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            logger.error(f"Query: {query}")
            if parameters:
                logger.error(f"Parameters: {parameters}")
            raise

    def run_query(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None,
        database: Optional[str] = None,
        fetch_all: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Execute a Cypher query and return the results as a list of dictionaries.
        This is an alias for execute_query with fetch_all=True for backward compatibility.

        Args:
            query: Cypher query string
            parameters: Query parameters
            database: Database name (optional)
            fetch_all: Whether to fetch all results (default: True)

        Returns:
            List of dictionaries containing the query results
        """
        return self.execute_query(query, parameters, database, fetch_all=fetch_all)

    def execute_query_single(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None,
        database: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Execute a Cypher query and return a single record.

        Args:
            query: Cypher query string
            parameters: Query parameters
            database: Target database name (if using multi-database setup)

        Returns:
            Dictionary representing a single record, or None if no records found
        """
        if parameters is None:
            parameters = {}

        try:
            with self.get_session(database) as session:
                result = session.run(query, parameters)
                record = result.single()
                return dict(record) if record else None
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            logger.error(f"Query: {query}")
            logger.error(f"Parameters: {parameters}")
            raise

    def execute_write_transaction(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None,
        database: Optional[str] = None,
    ) -> bool:
        """
        Execute a write transaction and return success status.

        Args:
            query: Cypher query string
            parameters: Query parameters
            database: Target database name (if using multi-database setup)

        Returns:
            True if successful, False otherwise
        """
        if parameters is None:
            parameters = {}

        try:
            with self.get_session(database) as session:
                result = session.execute_write(lambda tx: tx.run(query, parameters))
                return True
        except Exception as e:
            logger.error(f"Write transaction failed: {str(e)}")
            logger.error(f"Query: {query}")
            logger.error(f"Parameters: {parameters}")
            return False

    def get_session(self, database: Optional[str] = None) -> Session:
        """
        Get a new Neo4j session.

        Args:
            database: Target database name (if using multi-database setup)

        Returns:
            Neo4j Session object
        """
        if database:
            return self.driver.session(database=database)
        return self.driver.session()

    def create_constraints(self):
        """
        Create necessary constraints for the Synapse schema.
        """
        constraints = [
            "CREATE CONSTRAINT entity_name IF NOT EXISTS FOR (e:Entity) REQUIRE e.name IS UNIQUE",
            "CREATE CONSTRAINT belief_statement IF NOT EXISTS FOR (b:Belief) REQUIRE b.statement IS UNIQUE",
            "CREATE CONSTRAINT opinion_statement IF NOT EXISTS FOR (o:Opinion) REQUIRE o.statement IS UNIQUE",
            "CREATE CONSTRAINT source_name IF NOT EXISTS FOR (s:Source) REQUIRE s.name IS UNIQUE",
            "CREATE CONSTRAINT event_name IF NOT EXISTS FOR (e:Event) REQUIRE e.name IS UNIQUE",
            "CREATE CONSTRAINT concept_name IF NOT EXISTS FOR (c:Concept) REQUIRE c.name IS UNIQUE",
            "CREATE CONSTRAINT conflict_resolution_topic IF NOT EXISTS FOR (cr:ConflictResolution) REQUIRE cr.topic IS UNIQUE",
        ]

        with self.driver.session() as session:
            for constraint in constraints:
                try:
                    session.run(constraint)
                    logger.info(f"Created constraint: {constraint}")
                except Exception as e:
                    logger.warning(f"Failed to create constraint: {str(e)}")
