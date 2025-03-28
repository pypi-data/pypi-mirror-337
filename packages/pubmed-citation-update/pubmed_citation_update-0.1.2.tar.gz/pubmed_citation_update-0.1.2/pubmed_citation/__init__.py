__version__ = "0.1.2"  # Update version number to match setup.py

from pubmed_citation.scaffold import PubMedFetcher
from pubmed_citation.navigate import (
    find_path,
    compute_separation,
    find_all_connecting_papers,
    find_author_clusters,
)
from pubmed_citation.models import Article, Author, Network
