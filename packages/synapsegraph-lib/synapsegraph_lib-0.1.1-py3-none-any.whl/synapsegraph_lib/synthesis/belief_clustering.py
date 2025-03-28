import logging
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from synapsegraph_lib.core.models import Belief
from synapsegraph_lib.core.database import Neo4jConnection

logger = logging.getLogger(__name__)


class BeliefClusterer:
    """
    Clusters beliefs based on semantic similarity and relationships.
    Organizes beliefs into coherent clusters to improve knowledge organization.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the BeliefClusterer.

        Args:
            model_name: Name of the sentence transformer model to use for embeddings
        """
        try:
            self.model = SentenceTransformer(model_name)
            logger.info(f"Initialized BeliefClusterer with model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize sentence transformer model: {str(e)}")
            raise

        # Default clustering parameters
        self.eps = 0.3  # Maximum distance between samples in a cluster
        self.min_samples = 2  # Minimum number of samples in a cluster

    def cluster_beliefs(
        self, beliefs: List[Belief], eps: float = None, min_samples: int = None
    ) -> Dict[int, List[Belief]]:
        """
        Cluster beliefs based on semantic similarity.

        Args:
            beliefs: List of beliefs to cluster
            eps: Maximum distance between samples in a cluster (optional)
            min_samples: Minimum number of samples in a cluster (optional)

        Returns:
            Dictionary mapping cluster IDs to lists of beliefs
        """
        if not beliefs:
            logger.warning("No beliefs provided for clustering")
            return {}

        # Use provided parameters or defaults
        eps = eps if eps is not None else self.eps
        min_samples = min_samples if min_samples is not None else self.min_samples

        try:
            # Extract belief statements
            statements = [belief.statement for belief in beliefs]

            # Generate embeddings
            embeddings = self.model.encode(statements)

            # Perform clustering
            clustering = DBSCAN(eps=eps, min_samples=min_samples, metric="cosine").fit(
                embeddings
            )

            # Group beliefs by cluster
            clusters = {}
            for i, label in enumerate(clustering.labels_):
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(beliefs[i])

            # Count beliefs in each cluster
            cluster_counts = {
                label: len(beliefs_list) for label, beliefs_list in clusters.items()
            }
            logger.info(
                f"Clustered {len(beliefs)} beliefs into {len(clusters)} clusters: {cluster_counts}"
            )

            return clusters
        except Exception as e:
            logger.error(f"Error clustering beliefs: {str(e)}")
            return {-1: beliefs}  # Return all beliefs in a single "error" cluster

    def save_clusters_to_graph(
        self, db: Neo4jConnection, clusters: Dict[int, List[Belief]]
    ) -> Dict[int, str]:
        """
        Save belief clusters to the graph database.

        Args:
            db: Neo4j connection
            clusters: Dictionary mapping cluster IDs to lists of beliefs

        Returns:
            Dictionary mapping cluster IDs to cluster UIDs
        """
        cluster_uids = {}

        try:
            for cluster_id, beliefs in clusters.items():
                if cluster_id == -1:  # Skip noise cluster
                    continue

                # Create a cluster node
                cluster_name = self._generate_cluster_name(beliefs)

                query = """
                CREATE (c:BeliefCluster {
                    uid: randomUUID(),
                    name: $name,
                    size: $size,
                    created_at: datetime()
                })
                RETURN c.uid as uid
                """

                params = {"name": cluster_name, "size": len(beliefs)}

                result = db.execute_query(query, params)
                cluster_uid = result[0]["uid"] if result else None

                if not cluster_uid:
                    logger.error(
                        f"Failed to create cluster node for cluster {cluster_id}"
                    )
                    continue

                cluster_uids[cluster_id] = cluster_uid

                # Link beliefs to cluster
                for belief in beliefs:
                    link_query = """
                    MATCH (b:Belief {uid: $belief_uid})
                    MATCH (c:BeliefCluster {uid: $cluster_uid})
                    MERGE (b)-[:BELONGS_TO]->(c)
                    """

                    link_params = {"belief_uid": belief.uid, "cluster_uid": cluster_uid}

                    db.execute_query(link_query, link_params)

                logger.info(
                    f"Created cluster '{cluster_name}' with {len(beliefs)} beliefs"
                )

            return cluster_uids
        except Exception as e:
            logger.error(f"Error saving clusters to graph: {str(e)}")
            return {}

    def _generate_cluster_name(self, beliefs: List[Belief]) -> str:
        """
        Generate a descriptive name for a belief cluster.

        Args:
            beliefs: List of beliefs in the cluster

        Returns:
            Descriptive name for the cluster
        """
        if not beliefs:
            return "Empty Cluster"

        # Extract common entities or concepts
        # This is a simple implementation - could be enhanced with NLP
        common_words = self._extract_common_words([b.statement for b in beliefs])

        if common_words:
            return f"Cluster: {', '.join(common_words[:3])}"

        # Fallback: Use the highest confidence belief as the cluster name
        beliefs_sorted = sorted(beliefs, key=lambda b: b.confidence, reverse=True)
        return f"Cluster: {beliefs_sorted[0].statement[:50]}..."

    def _extract_common_words(
        self, statements: List[str], min_frequency: int = 2
    ) -> List[str]:
        """
        Extract common words from a list of statements.

        Args:
            statements: List of statements
            min_frequency: Minimum frequency for a word to be considered common

        Returns:
            List of common words
        """
        # Simple word frequency counter
        word_counts = {}

        for statement in statements:
            # Split statement into words and normalize
            words = statement.lower().split()

            # Count unique words in this statement
            statement_words = set(words)
            for word in statement_words:
                if len(word) > 3:  # Skip short words
                    word_counts[word] = word_counts.get(word, 0) + 1

        # Filter for common words
        common_words = [
            word for word, count in word_counts.items() if count >= min_frequency
        ]

        # Sort by frequency
        common_words.sort(key=lambda w: word_counts[w], reverse=True)

        return common_words

    def find_related_clusters(
        self, db: Neo4jConnection, belief: Belief, max_clusters: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Find clusters related to a given belief.

        Args:
            db: Neo4j connection
            belief: Belief to find related clusters for
            max_clusters: Maximum number of clusters to return

        Returns:
            List of related clusters with metadata
        """
        try:
            # First check if the belief belongs to any clusters
            direct_query = """
            MATCH (b:Belief {uid: $belief_uid})-[:BELONGS_TO]->(c:BeliefCluster)
            RETURN c.uid as uid, c.name as name, c.size as size
            """

            direct_params = {"belief_uid": belief.uid}
            direct_results = db.execute_query(
                direct_query, direct_params, fetch_all=True
            )

            if direct_results:
                return [dict(result) for result in direct_results]

            # If not, find semantically similar clusters
            # Get all cluster names
            clusters_query = """
            MATCH (c:BeliefCluster)
            RETURN c.uid as uid, c.name as name, c.size as size
            """

            clusters = db.execute_query(clusters_query, {}, fetch_all=True)

            if not clusters:
                return []

            # Generate embeddings
            cluster_names = [cluster["name"] for cluster in clusters]
            cluster_embeddings = self.model.encode(cluster_names)
            belief_embedding = self.model.encode([belief.statement])[0]

            # Calculate similarities
            similarities = cosine_similarity([belief_embedding], cluster_embeddings)[0]

            # Sort clusters by similarity
            sorted_indices = np.argsort(similarities)[::-1][:max_clusters]

            related_clusters = []
            for idx in sorted_indices:
                if similarities[idx] > 0.5:  # Minimum similarity threshold
                    cluster_data = dict(clusters[idx])
                    cluster_data["similarity"] = float(similarities[idx])
                    related_clusters.append(cluster_data)

            return related_clusters
        except Exception as e:
            logger.error(f"Error finding related clusters: {str(e)}")
            return []

    def merge_similar_clusters(
        self, db: Neo4jConnection, similarity_threshold: float = 0.8
    ) -> int:
        """
        Merge similar clusters to maintain a clean knowledge organization.

        Args:
            db: Neo4j connection
            similarity_threshold: Minimum similarity for clusters to be merged

        Returns:
            Number of clusters merged
        """
        try:
            # Get all clusters
            clusters_query = """
            MATCH (c:BeliefCluster)
            RETURN c.uid as uid, c.name as name
            """

            clusters = db.execute_query(clusters_query, {}, fetch_all=True)

            if not clusters or len(clusters) < 2:
                return 0

            # Generate embeddings for cluster names
            cluster_names = [cluster["name"] for cluster in clusters]
            embeddings = self.model.encode(cluster_names)

            # Calculate pairwise similarities
            similarities = cosine_similarity(embeddings)

            # Find clusters to merge
            merged_count = 0
            processed_clusters = set()

            for i in range(len(clusters)):
                if i in processed_clusters:
                    continue

                cluster_i = clusters[i]

                for j in range(i + 1, len(clusters)):
                    if j in processed_clusters:
                        continue

                    cluster_j = clusters[j]

                    if similarities[i, j] >= similarity_threshold:
                        # Merge cluster j into cluster i
                        merge_query = """
                        MATCH (c1:BeliefCluster {uid: $uid1})
                        MATCH (c2:BeliefCluster {uid: $uid2})
                        MATCH (b:Belief)-[:BELONGS_TO]->(c2)
                        MERGE (b)-[:BELONGS_TO]->(c1)
                        WITH c1, c2, count(b) as belief_count
                        SET c1.size = c1.size + belief_count
                        DETACH DELETE c2
                        """

                        merge_params = {
                            "uid1": cluster_i["uid"],
                            "uid2": cluster_j["uid"],
                        }

                        db.execute_query(merge_query, merge_params)
                        processed_clusters.add(j)
                        merged_count += 1

                        logger.info(
                            f"Merged cluster '{cluster_j['name']}' into '{cluster_i['name']}'"
                        )

            return merged_count
        except Exception as e:
            logger.error(f"Error merging similar clusters: {str(e)}")
            return 0
