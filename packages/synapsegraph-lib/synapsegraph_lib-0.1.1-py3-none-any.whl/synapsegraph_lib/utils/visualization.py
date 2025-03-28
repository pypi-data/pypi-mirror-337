"""
Visualization utilities for SynapseGraph.

This module provides functionality for visualizing the knowledge graph,
including node and relationship visualization.
"""

import logging
from typing import Dict, List, Any, Optional, Set

logger = logging.getLogger(__name__)


class GraphVisualization:
    """
    Graph visualization class for SynapseGraph.

    This class provides basic functionality for generating graph visualizations,
    primarily for command-line display but could be extended for GUI or web interfaces.
    """

    @staticmethod
    def text_graph(
        nodes: List[Dict], relationships: List[Dict], max_depth: int = 2
    ) -> str:
        """
        Generate a text-based representation of a graph.

        Args:
            nodes: List of node dictionaries
            relationships: List of relationship dictionaries
            max_depth: Maximum depth to display

        Returns:
            String representation of the graph
        """
        if not nodes:
            return "Empty graph"

        # Start with the first node as root
        root = nodes[0]

        # Build a simple adjacency list
        adjacency = {}
        for node in nodes:
            adjacency[node["uid"]] = []

        for rel in relationships:
            if rel["source"] in adjacency:
                adjacency[rel["source"]].append(
                    {"target": rel["target"], "type": rel["type"]}
                )

        # Generate the text representation
        lines = []
        visited = set()

        def dfs(node_id, depth, prefix):
            if depth > max_depth or node_id in visited:
                return

            visited.add(node_id)

            # Find the node details
            node_details = next((n for n in nodes if n["uid"] == node_id), None)
            if not node_details:
                return

            # Add this node to the output
            node_type = node_details.get("label", "Node")
            node_name = node_details.get("name", node_details.get("statement", node_id))
            lines.append(f"{prefix}├── {node_type}: {node_name}")

            # Process children
            for i, rel in enumerate(adjacency[node_id]):
                is_last = i == len(adjacency[node_id]) - 1
                new_prefix = prefix + ("    " if is_last else "│   ")
                dfs(rel["target"], depth + 1, new_prefix)

        # Start the traversal
        dfs(root["uid"], 0, "")

        return "\n".join(lines)

    @staticmethod
    def summarize_graph(nodes: List[Dict], relationships: List[Dict]) -> Dict[str, Any]:
        """
        Generate a summary of the graph.

        Args:
            nodes: List of node dictionaries
            relationships: List of relationship dictionaries

        Returns:
            Dictionary with graph summary statistics
        """
        node_types = {}
        for node in nodes:
            node_type = node.get("label", "Unknown")
            node_types[node_type] = node_types.get(node_type, 0) + 1

        rel_types = {}
        for rel in relationships:
            rel_type = rel.get("type", "Unknown")
            rel_types[rel_type] = rel_types.get(rel_type, 0) + 1

        return {
            "total_nodes": len(nodes),
            "total_relationships": len(relationships),
            "node_types": node_types,
            "relationship_types": rel_types,
        }


# Convenience function for external use
def graph_visualization(nodes: List[Dict], relationships: List[Dict]) -> str:
    """
    Generate a text visualization of a graph.

    Args:
        nodes: List of node dictionaries
        relationships: List of relationship dictionaries

    Returns:
        String representation of the graph
    """
    visualizer = GraphVisualization()
    return visualizer.text_graph(nodes, relationships)
