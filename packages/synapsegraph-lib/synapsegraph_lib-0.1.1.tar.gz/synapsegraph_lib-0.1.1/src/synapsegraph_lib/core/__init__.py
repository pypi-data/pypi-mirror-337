"""
Core components of the SynapseGraph system.

This module contains the fundamental classes and utilities that form
the backbone of the SynapseGraph system.
"""

from synapsegraph_lib.core.synapse_graph import SynapseGraph
from synapsegraph_lib.core.models import Entity, Belief, Opinion
from synapsegraph_lib.core.database import Neo4jConnection
from synapsegraph_lib.core.retrieval import KnowledgeRetrieval
from synapsegraph_lib.core.config import OpinionStance, TimeHorizon

__all__ = [
    "SynapseGraph",
    "Entity",
    "Belief",
    "Opinion",
    "Neo4jConnection",
    "KnowledgeRetrieval",
    "OpinionStance",
    "TimeHorizon",
]
