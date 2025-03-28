import requests
import time
import xml.etree.ElementTree as ET
import json
import os
from collections import deque
from urllib.parse import quote_plus
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

from pubmed_citation.models import Article, Author, Network


class RateLimiter:
    """Simple rate limiter to prevent exceeding API rate limits."""

    def __init__(self, rate_limit=3, per_seconds=1):
        self.rate_limit = rate_limit
        self.per_seconds = per_seconds
        self.request_times = deque()

    def wait(self):
        """Wait if necessary to respect the rate limit."""
        current_time = time.time()

        # Remove request times outside our window
        while (
            self.request_times
            and self.request_times[0] <= current_time - self.per_seconds
        ):
            self.request_times.popleft()

        # If at limit, wait until we can make another request
        if len(self.request_times) >= self.rate_limit:
            sleep_time = self.request_times[0] + self.per_seconds - current_time
            if sleep_time > 0:
                time.sleep(sleep_time)
                current_time = time.time()

        # Add the current request time
        self.request_times.append(current_time)


class PubMedFetcher:
    """Handles fetching citation data from PubMed using the E-utilities API."""

    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

    def __init__(self, email=None, api_key=None, cache_dir="pubmed_cache"):
        """
        Initialize the PubMed fetcher.

        Args:
            email (str): User's email (recommended by NCBI)
            api_key (str): NCBI API key for higher rate limits
            cache_dir (str): Directory to store cached results
        """
        self.email = email
        self.api_key = api_key
        self.cache_dir = cache_dir

        # Create cache directory if it doesn't exist
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        # Initialize rate limiter
        # With API key: 10 requests per second, without: 3 requests per second
        rate_limit = 10 if api_key else 3
        self.rate_limiter = RateLimiter(rate_limit=rate_limit, per_seconds=1)

    def search_articles(
        self,
        query,
        max_results=50,
        date_from=None,
        date_to=None,
        language="english",
        use_cache=True,
    ):
        """
        Search for articles in PubMed that match the query.

        Args:
            query (str): The search query
            max_results (int): Maximum number of results to return
            date_from (str): Start date in format YYYY/MM/DD
            date_to (str): End date in format YYYY/MM/DD
            language (str): Language filter
            use_cache (bool): Whether to use cached results

        Returns:
            list: List of Article objects
        """
        # Create a cache key
        cache_key = f"search_{hash(f'{query}_{max_results}_{date_from}_{date_to}_{language}')}.json"
        cache_path = os.path.join(self.cache_dir, cache_key)

        # Check for cached results
        if use_cache and os.path.exists(cache_path):
            with open(cache_path, "r") as f:
                pmids = json.load(f)
            logger.info(f"Loaded {len(pmids)} results from cache")
        else:
            # Construct query with filters
            search_query = query

            if language:
                search_query += f" AND {language}[lang]"

            if date_from and date_to:
                search_query += f" AND {date_from}:{date_to}[pdat]"
            elif date_from:
                search_query += f" AND {date_from}[pdat]"
            elif date_to:
                search_query += f" AND {date_to}[pdat]"

            # Get the list of PMIDs that match the query
            params = {
                "db": "pubmed",
                "term": search_query,
                "retmax": max_results,
                "retmode": "json",
                "sort": "relevance",
            }

            if self.email:
                params["email"] = self.email

            if self.api_key:
                params["api_key"] = self.api_key

            # Apply rate limiting
            self.rate_limiter.wait()

            try:
                response = requests.get(f"{self.BASE_URL}esearch.fcgi", params=params)
                response.raise_for_status()
                data = response.json()
                pmids = data["esearchresult"]["idlist"]

                # Cache the PMIDs
                with open(cache_path, "w") as f:
                    json.dump(pmids, f)

                logger.info(f"Found {len(pmids)} matching articles")
            except Exception as e:
                logger.error(f"Error searching PubMed: {e}")
                return []

        # Fetch article details
        articles = self.fetch_articles_by_pmid(pmids, use_cache)

        return articles

    def fetch_articles_by_pmid(self, pmids, use_cache=True):
        """
        Fetch article details for a list of PMIDs.

        Args:
            pmids (list): List of PubMed IDs
            use_cache (bool): Whether to use cached results

        Returns:
            list: List of Article objects
        """
        if not pmids:
            return []

        # Create a cache key
        pmids_str = "_".join(sorted(pmids))
        cache_key = f"articles_{hash(pmids_str)}.json"
        cache_path = os.path.join(self.cache_dir, cache_key)

        # Check for cached results
        if use_cache and os.path.exists(cache_path):
            with open(cache_path, "r") as f:
                article_data = json.load(f)

            # Convert from dict to Article objects
            articles = []
            for data in article_data:
                try:
                    articles.append(Article.from_dict(data))
                except Exception as e:
                    logger.error(f"Error deserializing article: {e}")

            return articles

        # Process in batches to avoid overloading the API
        all_articles = []
        batch_size = 50

        for i in range(0, len(pmids), batch_size):
            batch_pmids = pmids[i : i + batch_size]

            # Prepare API request
            params = {
                "db": "pubmed",
                "id": ",".join(batch_pmids),
                "retmode": "xml",
                "rettype": "abstract",
            }

            if self.email:
                params["email"] = self.email

            if self.api_key:
                params["api_key"] = self.api_key

            # Apply rate limiting
            self.rate_limiter.wait()

            try:
                response = requests.get(f"{self.BASE_URL}efetch.fcgi", params=params)
                response.raise_for_status()
                batch_articles = self._parse_pubmed_xml(response.text)
                all_articles.extend(batch_articles)
            except Exception as e:
                logger.error(f"Error fetching articles: {e}")
                continue

        # Cache the results
        article_data = [article.to_dict() for article in all_articles]
        with open(cache_path, "w") as f:
            json.dump(article_data, f)

        return all_articles

    def _parse_pubmed_xml(self, xml_text):
        """
        Parse PubMed XML response into Article objects.

        Args:
            xml_text (str): XML response from PubMed

        Returns:
            list: List of Article objects
        """
        articles = []

        try:
            root = ET.fromstring(xml_text)

            for article_element in root.findall(".//PubmedArticle"):
                try:
                    # Get PMID
                    pmid_element = article_element.find(".//PMID")
                    if pmid_element is None:
                        continue
                    pmid = pmid_element.text

                    # Get title
                    title_element = article_element.find(".//ArticleTitle")
                    title = (
                        title_element.text
                        if title_element is not None
                        else "Unknown Title"
                    )

                    # Get journal
                    journal_element = article_element.find(".//Journal/Title")
                    journal = (
                        journal_element.text if journal_element is not None else ""
                    )

                    # Get publication date
                    year_element = article_element.find(".//PubDate/Year")
                    year = year_element.text if year_element is not None else None

                    month_element = article_element.find(".//PubDate/Month")
                    month = month_element.text if month_element is not None else "1"

                    day_element = article_element.find(".//PubDate/Day")
                    day = day_element.text if day_element is not None else "1"

                    # Create date string if year is available
                    date = None
                    if year:
                        try:
                            date = f"{year}-{month}-{day}"
                        except:
                            date = f"{year}-01-01"

                    # Get authors
                    authors = []
                    author_elements = article_element.findall(".//Author")

                    for author_elem in author_elements:
                        last_name = author_elem.find("LastName")
                        fore_name = author_elem.find("ForeName")

                        if last_name is not None or fore_name is not None:
                            last = last_name.text if last_name is not None else ""
                            fore = fore_name.text if fore_name is not None else ""

                            name = f"{fore} {last}".strip()
                            identifier = name.lower().replace(" ", "")

                            author = Author(identifier=identifier, name=name)
                            authors.append(author)

                    # Create article object
                    article = Article(
                        pmid=pmid,
                        title=title,
                        journal=journal,
                        date=date,
                        authors=authors,
                        citations=[],
                    )

                    articles.append(article)

                except Exception as e:
                    logger.error(f"Error parsing article element: {e}")
                    continue

        except ET.ParseError as e:
            logger.error(f"XML parse error: {e}")

        return articles

    def build_citation_network(
        self,
        query,
        max_results=50,
        depth=1,
        date_from=None,
        date_to=None,
        language="english",
        use_cache=True,
    ):
        """
        Build a citation network starting from the search results.

        Args:
            query (str): The search query
            max_results (int): Maximum number of top-level results
            depth (int): How many levels of citations to fetch
            date_from (str): Start date in format YYYY/MM/DD
            date_to (str): End date in format YYYY/MM/DD
            language (str): Language filter
            use_cache (bool): Whether to use cached results

        Returns:
            Network: A network of articles, authors, and their relationships
        """
        # Create a cache key
        cache_key = f"network_{hash(f'{query}_{max_results}_{depth}_{date_from}_{date_to}_{language}')}.json"
        cache_path = os.path.join(self.cache_dir, cache_key)

        # Check for cached network
        if use_cache and os.path.exists(cache_path):
            try:
                with open(cache_path, "r") as f:
                    network_data = json.load(f)
                network = Network.from_dict(network_data)
                logger.info(
                    f"Loaded network from cache with {len(network.articles)} articles"
                )
                return network
            except Exception as e:
                logger.error(f"Error loading cached network: {e}")
                # Continue with building new network

        # First get the seed articles
        seed_articles = self.search_articles(
            query=query,
            max_results=max_results,
            date_from=date_from,
            date_to=date_to,
            language=language,
            use_cache=use_cache,
        )

        # Initialize the network
        network = Network()
        for article in seed_articles:
            network.add_article(article)

        # Fetch citations if depth > 0
        processed_pmids = set()
        to_process = [
            (article.pmid, 0) for article in seed_articles
        ]  # (pmid, current_depth)

        while to_process:
            pmid, current_depth = to_process.pop(0)

            if pmid in processed_pmids or current_depth >= depth:
                continue

            processed_pmids.add(pmid)

            # Get citations
            citing_pmids = self._get_citing_articles(pmid, use_cache)

            # Process each citing article
            if citing_pmids:
                citing_articles = self.fetch_articles_by_pmid(citing_pmids, use_cache)

                for citing_article in citing_articles:
                    # Add to network
                    network.add_article(citing_article)
                    network.add_citation(citing_article.pmid, pmid)

                    # Add to processing queue for next level
                    if current_depth + 1 < depth:
                        to_process.append((citing_article.pmid, current_depth + 1))

        # Cache the network
        try:
            with open(cache_path, "w") as f:
                json.dump(network.to_dict(), f)
        except Exception as e:
            logger.error(f"Error caching network: {e}")

        return network

    def _get_citing_articles(self, pmid, use_cache=True):
        """
        Get the PMIDs of articles that cite a given article.

        Args:
            pmid (str): The PMID of the article
            use_cache (bool): Whether to use cached results

        Returns:
            list: List of citing PMIDs
        """
        # Create a cache key
        cache_key = f"citations_{pmid}.json"
        cache_path = os.path.join(self.cache_dir, cache_key)

        # Check for cached results
        if use_cache and os.path.exists(cache_path):
            with open(cache_path, "r") as f:
                citing_pmids = json.load(f)
            return citing_pmids

        # Get citations using E-link
        params = {
            "dbfrom": "pubmed",
            "db": "pubmed",
            "id": pmid,
            "cmd": "neighbor_history",
            "linkname": "pubmed_pubmed_citedin",  # Articles that cite this one
        }

        if self.email:
            params["email"] = self.email

        if self.api_key:
            params["api_key"] = self.api_key

        # Apply rate limiting
        self.rate_limiter.wait()

        try:
            response = requests.get(f"{self.BASE_URL}elink.fcgi", params=params)
            response.raise_for_status()

            # Parse XML to get the query key and WebEnv
            root = ET.fromstring(response.text)
            query_key_element = root.find(".//QueryKey")
            webenv_element = root.find(".//WebEnv")

            if query_key_element is None or webenv_element is None:
                logger.info(f"No citations found for {pmid}")
                citing_pmids = []
            else:
                query_key = query_key_element.text
                webenv = webenv_element.text

                # Fetch the citation PMIDs
                fetch_params = {
                    "db": "pubmed",
                    "query_key": query_key,
                    "WebEnv": webenv,
                    "retmax": 100,  # Limit number of citations
                    "retmode": "json",
                }

                if self.email:
                    fetch_params["email"] = self.email

                if self.api_key:
                    fetch_params["api_key"] = self.api_key

                # Apply rate limiting
                self.rate_limiter.wait()

                fetch_response = requests.get(
                    f"{self.BASE_URL}esummary.fcgi", params=fetch_params
                )
                fetch_response.raise_for_status()

                try:
                    citation_data = fetch_response.json()
                    citing_pmids = list(citation_data.get("result", {}).keys())
                    # Remove uids key which isn't a PMID
                    if "uids" in citing_pmids:
                        citing_pmids.remove("uids")
                except:
                    logger.error(f"Error parsing citation response for {pmid}")
                    citing_pmids = []
        except Exception as e:
            logger.error(f"Error fetching citations for {pmid}: {e}")
            citing_pmids = []

        # Cache the citation PMIDs
        with open(cache_path, "w") as f:
            json.dump(citing_pmids, f)

        return citing_pmids

    def get_author_publications(self, author_name, max_results=50, use_cache=True):
        """
        Get publications for a specific author.

        Args:
            author_name (str): The name of the author
            max_results (int): Maximum number of results
            use_cache (bool): Whether to use cached results

        Returns:
            list: List of Article objects
        """
        # Construct a query for the author
        query = f"{author_name}[Author]"
        return self.search_articles(query, max_results, use_cache=use_cache)
