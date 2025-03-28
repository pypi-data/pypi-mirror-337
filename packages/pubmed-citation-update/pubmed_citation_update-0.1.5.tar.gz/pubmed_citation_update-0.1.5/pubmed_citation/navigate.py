from collections import deque
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def find_path(network, author1_id, author2_id, algorithm="bfs"):
    """
    Find the shortest path between two authors in the co-authorship network.

    Args:
        network (Network): The network
        author1_id (str): Identifier of the first author
        author2_id (str): Identifier of the second author
        algorithm (str): "bfs" for breadth-first search or "dfs" for depth-first search

    Returns:
        list: List of author IDs in the path, or None if no path exists
    """
    if author1_id == author2_id:
        return [author1_id]

    if author1_id not in network.authors or author2_id not in network.authors:
        logger.warning(f"One or both authors not found in network")
        return None

    if algorithm.lower() == "bfs":
        return _bfs_path(network, author1_id, author2_id)
    elif algorithm.lower() == "dfs":
        return _dfs_path(network, author1_id, author2_id)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")


def _bfs_path(network, start_id, end_id):
    """Find the shortest path using breadth-first search."""
    queue = deque([(start_id, [start_id])])
    visited = set([start_id])

    while queue:
        current_id, path = queue.popleft()

        if current_id == end_id:
            return path

        for neighbor_id in network.get_coauthors(current_id):
            if neighbor_id not in visited:
                visited.add(neighbor_id)
                queue.append((neighbor_id, path + [neighbor_id]))

    return None


def _dfs_path(network, start_id, end_id):
    """Find a path using depth-first search."""
    stack = [(start_id, [start_id])]
    visited = set()

    while stack:
        current_id, path = stack.pop()

        if current_id == end_id:
            return path

        if current_id not in visited:
            visited.add(current_id)

            for neighbor_id in network.get_coauthors(current_id):
                if neighbor_id not in visited:
                    stack.append((neighbor_id, path + [neighbor_id]))

    return None


def compute_separation(network, author1_id, author2_id):
    """
    Compute the degrees of separation between two authors.

    Args:
        network (Network): The network
        author1_id (str): Identifier of the first author
        author2_id (str): Identifier of the second author

    Returns:
        int: Degrees of separation (path length - 1), or None if no path exists
    """
    path = find_path(network, author1_id, author2_id)

    if path is None:
        return None

    # Degrees of separation is the number of edges in the path,
    # which is one less than the number of nodes
    return len(path) - 1


def find_all_connecting_papers(network, author1_id, author2_id):
    """
    Find all papers connecting two authors.

    Args:
        network (Network): The network
        author1_id (str): Identifier of the first author
        author2_id (str): Identifier of the second author

    Returns:
        list: List of PMIDs for papers co-authored by both authors
    """
    if author1_id not in network.authors or author2_id not in network.authors:
        return []

    author1 = network.authors[author1_id]
    author2 = network.authors[author2_id]

    # Find intersection of their articles
    return list(set(author1.articles) & set(author2.articles))


def find_author_clusters(network, min_size=2):
    """
    Find clusters of authors who frequently collaborate.

    Args:
        network (Network): The network
        min_size (int): Minimum cluster size

    Returns:
        list: List of author clusters, where each cluster is a list of author IDs
    """
    # Simple clustering based on connected components
    clusters = []
    unvisited = set(network.authors.keys())

    while unvisited:
        # Start a new cluster with an unvisited author
        current = next(iter(unvisited))
        cluster = []

        # Use BFS to find all connected authors
        queue = deque([current])
        visited = set([current])

        while queue:
            author_id = queue.popleft()
            cluster.append(author_id)

            for coauthor_id in network.get_coauthors(author_id):
                if coauthor_id not in visited:
                    visited.add(coauthor_id)
                    queue.append(coauthor_id)

        # Add the cluster if it meets the minimum size
        if len(cluster) >= min_size:
            clusters.append(cluster)

        # Update unvisited set
        unvisited -= set(cluster)

    return clusters
