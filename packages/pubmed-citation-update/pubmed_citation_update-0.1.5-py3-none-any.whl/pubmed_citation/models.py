import  numpy as np
from scipy import sparse
import logging
import signal
import time

logger = logging.getLogger(__name__)

class Author:
    """Represents an author of a scientific article."""

    def __init__(self, identifier, name, articles=None):
        """
        Initialize an author.

        Args:
            identifier (str): Unique identifier for the author
            name (str): Author's full name
            articles (list, optional): List of article PMIDs authored by this person
        """
        self.identifier = identifier
        self.name = name
        self.articles = articles or []

    def __str__(self):
        """String representation of the author."""
        return self.name

    def to_dict(self):
        """Convert to dictionary for serialization."""
        return {
            "identifier": self.identifier,
            "name": self.name,
            "articles": self.articles,
        }

    @classmethod
    def from_dict(cls, data):
        """Create an Author from a dictionary."""
        return cls(
            identifier=data["identifier"],
            name=data["name"],
            articles=data.get("articles", []),
        )


class Article:
    """Represents a scientific article with its metadata."""

    def __init__(
        self, pmid, title, journal=None, date=None, authors=None, citations=None
    ):
        """
        Initialize an article.

        Args:
            pmid (str): PubMed ID
            title (str): Article title
            journal (str, optional): Journal name
            date (str, optional): Publication date
            authors (list, optional): List of Author objects
            citations (list, optional): List of citation PMIDs
        """
        self.pmid = pmid
        self.title = title
        self.journal = journal or ""
        self.date = date
        self.authors = authors or []
        self.citations = citations or []

    def __str__(self):
        """String representation of the article."""
        return f"{self.title} (PMID: {self.pmid})"

    def to_dict(self):
        """Convert to dictionary for serialization."""
        return {
            "pmid": self.pmid,
            "title": self.title,
            "journal": self.journal,
            "date": self.date,
            "authors": [author.to_dict() for author in self.authors],
            "citations": self.citations,
        }

    @classmethod
    def from_dict(cls, data):
        """Create an Article from a dictionary."""
        authors = []
        for author_data in data.get("authors", []):
            authors.append(Author.from_dict(author_data))

        return cls(
            pmid=data["pmid"],
            title=data["title"],
            journal=data.get("journal", ""),
            date=data.get("date"),
            authors=authors,
            citations=data.get("citations", []),
        )


class Network:
    """Represents a network of articles, authors, and their relationships."""

    def __init__(self):
        """Initialize an empty network."""
        self.articles = {}  # PMID -> Article
        self.authors = {}  # ID -> Author
        self.citations = {}  # cited PMID -> list of citing PMIDs
        self.coauthorships = {}  # author ID -> set of co-author IDs
        self.adjacency_matrix = None
        self.author_index_map = None

    def add_article(self, article):
        """Add an article to the network."""
        self.articles[article.pmid] = article

        # Add authors and co-authorship relationships
        for author in article.authors:
            self.add_author(author)
            author.articles.append(article.pmid)

            # Add co-authorship
            if author.identifier not in self.coauthorships:
                self.coauthorships[author.identifier] = set()

            for coauthor in article.authors:
                if coauthor.identifier != author.identifier:
                    self.coauthorships[author.identifier].add(coauthor.identifier)

    def add_author(self, author):
        """Add an author to the network if not already present."""
        if author.identifier not in self.authors:
            self.authors[author.identifier] = author

    def add_citation(self, citing_pmid, cited_pmid):
        """Add a citation relationship between articles."""
        if cited_pmid not in self.citations:
            self.citations[cited_pmid] = []

        if citing_pmid not in self.citations[cited_pmid]:
            self.citations[cited_pmid].append(citing_pmid)

    def get_coauthors(self, author_id):
        """Get the co-authors of an author."""
        return list(self.coauthorships.get(author_id, set()))

    def export_to_csv(
        self, articles_file, citations_file, authors_file=None, coauthorship_file=None
    ):
        """Export the network to CSV files for external analysis."""
        import csv

        # Export articles
        with open(articles_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["pmid", "title", "journal", "date", "num_authors"])

            for pmid, article in self.articles.items():
                writer.writerow(
                    [
                        pmid,
                        article.title,
                        article.journal,
                        article.date,
                        len(article.authors),
                    ]
                )

        # Export citations
        with open(citations_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["citing_pmid", "cited_pmid"])

            for cited_pmid, citing_pmids in self.citations.items():
                for citing_pmid in citing_pmids:
                    writer.writerow([citing_pmid, cited_pmid])

        # Export authors if requested
        if authors_file:
            with open(authors_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["id", "name", "article_count"])

                for author_id, author in self.authors.items():
                    writer.writerow([author_id, author.name, len(author.articles)])

        # Export co-authorship if requested
        if coauthorship_file:
            with open(coauthorship_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["author1", "author2"])

                for author_id, coauthors in self.coauthorships.items():
                    for coauthor_id in coauthors:
                        if author_id < coauthor_id:  # Avoid duplicates
                            writer.writerow([author_id, coauthor_id])

        return True

    def to_dict(self):
        """Convert to dictionary for serialization."""
        return {
            "articles": {
                pmid: article.to_dict() for pmid, article in self.articles.items()
            },
            "citations": self.citations,
            "coauthorships": {
                author_id: list(coauthors)
                for author_id, coauthors in self.coauthorships.items()
            },
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Network from a dictionary."""
        network = cls()

        # Add articles
        for pmid, article_data in data.get("articles", {}).items():
            network.add_article(Article.from_dict(article_data))

        # Add citations
        for cited_pmid, citing_pmids in data.get("citations", {}).items():
            for citing_pmid in citing_pmids:
                network.add_citation(citing_pmid, cited_pmid)

        # Add coauthorships
        for author_id, coauthors in data.get("coauthorships", {}).items():
            if author_id not in network.coauthorships:
                network.coauthorships[author_id] = set()

            for coauthor_id in coauthors:
                network.coauthorships[author_id].add(coauthor_id)

        return network

    def create_adjacency_matrix(self):
        """Creates and stores adjacency matrix for coauthorship network"""
        
        if not self.authors:
            raise ValueError("Cannot create adjacency matrix: network has no authors")
          
        # Create mapping from author IDs to matrix indices
        author_ids = list(self.authors.keys())
        self.author_index_map = {author_id: idx for idx, author_id in enumerate(author_ids)}
        
        # Initialize lists for sparse matrix construction
        rows = []
        cols = []
        data = []
        
        # Fill data for sparse matrix based on coauthorships
        for author_id, coauthors in self.coauthorships.items():
            i = self.author_index_map[author_id]
            for coauthor_id in coauthors:
                j = self.author_index_map[coauthor_id]
                rows.extend([i, j])
                cols.extend([j, i]) 
                data.extend([1, 1])
                
        n = len(author_ids)
        self.adjacency_matrix = sparse.csr_matrix((data, (rows, cols)), shape=(n, n))
        return self.adjacency_matrix, self.author_index_map

    def create_degree_matrix(self):
        """Creates and stores degree matrix for coauthorship network"""    
        
        if not self.authors:
            raise ValueError("Cannot create degree matrix: network has no authors")
        
        # Use existing mapping or create new one
        if not self.author_index_map:
            author_ids = list(self.authors.keys())
            self.author_index_map = {author_id: idx for idx, author_id in enumerate(author_ids)}
        
        # Initialize data for sparse diagonal matrix
        n = len(self.authors)
        degrees = [len(self.get_coauthors(author_id)) for author_id in self.authors]
        self.degree_matrix = sparse.diags(degrees)
            
        return self.degree_matrix
        
    def _kmeans(self, points, k, max_iters=100):
        """
        Manual implementation of k-means clustering.
        
        Args:
            points (np.ndarray): Matrix where each row is a point to cluster
            k (int): Number of clusters
            max_iters (int): Maximum iterations before forced termination
            
        Returns:
            np.ndarray: Cluster assignments for each point
        """
        n_points = points.shape[0]
        
        # Initialize random centroids from points
        rng = np.random.default_rng(42)
        centroid_indices = rng.choice(n_points, k, replace=False)
        centroids = points[centroid_indices]
        
        prev_assignments = None
        
        for _ in range(max_iters):
            # Calculate distances to centroids
            distances = np.zeros((n_points, k))
            for i in range(k):
                distances[:,i] = np.sum((points - centroids[i])**2, axis=1)
                
            # Assign points to nearest centroid
            assignments = np.argmin(distances, axis=1)
            
            # Check convergence
            if prev_assignments is not None and np.all(assignments == prev_assignments):
                break
                
            # Update centroids
            for i in range(k):
                points_in_cluster = points[assignments == i]
                if len(points_in_cluster) > 0:
                    centroids[i] = np.mean(points_in_cluster, axis=0)
                    
            prev_assignments = assignments
            
        return assignments

    def spectral_clustering(self, k):
        """
        Perform spectral clustering to group authors into k clusters.
        
        Args:
            k (int): Number of desired clusters
            
        Returns:
            dict: Mapping of author IDs to cluster numbers
        """
        
        # Ensure matrices exist
        if self.adjacency_matrix is None:
            logger.info('creating adjacency matrix')  
            self.create_adjacency_matrix()
        if not hasattr(self, 'degree_matrix'):
            logger.info('creating degree matrix')
            self.create_degree_matrix()
            
        # Calculate Laplacian
        laplacian = self.degree_matrix - self.adjacency_matrix
        
        logger.info('calculating eigenvalues and eignvectors')
        # Use sparse eigenvalue solver for k+1 smallest eigenvalues
        def timeout_handler(signum, frame):
            raise TimeoutError("Computation took too long")

        # Set timeout of 30 seconds
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(30)

        try:
            eigenvalues, eigenvectors = sparse.linalg.eigsh(laplacian, k=k+1, which='SM')
            signal.alarm(0)  # Disable alarm
        except TimeoutError:
            logger.warning(f"Spectral clustering too slow for matrix of size {laplacian.shape}. Try reducing the network size.")
            raise ValueError("Matrix too large for efficient clustering")
        
        # Sort eigenvalues and get indices of k smallest non-zero values
        sorted_indices = np.argsort(eigenvalues)[1:k+1]  # Skip smallest (zero) eigenvalue
        
        # Form matrix U with k eigenvectors
        U = eigenvectors[:, sorted_indices]
        
        logger.info('running kmeans')
        # Perform k-means on rows of U
        cluster_labels = self._kmeans(U, k)
        
        # Map results back to authors
        author_clusters = {}
        for author_id, idx in self.author_index_map.items():
            author_clusters[author_id] = int(cluster_labels[idx])
            
        return author_clusters
