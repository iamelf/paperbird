"""
ArXiv Paper Fetcher

This module fetches the latest papers from arXiv and extracts relevant information
such as title, abstract, and authors.
"""

import datetime
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

import feedparser
import requests


class ArxivFetcher:
    """
    A class to fetch and parse arXiv papers.
    """

    BASE_URL = "http://export.arxiv.org/api/query?"

    def __init__(
        self,
        default_search_term: str = "all:quantum",
        default_category: str = "cs",
        default_subcategory: str = "cs.AI",
        default_max_results: int = 50,
        default_sort_by: str = "submittedDate",
        default_sort_order: str = "descending",
    ):
        """
        Initialize the ArxivFetcher with default values.

        Args:
            default_search_term: Default search term to use when none is provided
            default_category: Default arXiv category (e.g., 'cs' for Computer Science)
            default_subcategory: Default arXiv subcategory (e.g., 'cs.AI' for Artificial Intelligence)
            default_max_results: Default maximum number of results to return
            default_sort_by: Default field to sort by ('submittedDate', 'relevance', etc.)
            default_sort_order: Default order of sorting ('ascending' or 'descending')
        """
        self.default_search_term = default_search_term
        self.default_category = default_category
        self.default_subcategory = default_subcategory
        self.default_max_results = default_max_results
        self.default_sort_by = default_sort_by
        self.default_sort_order = default_sort_order

    def fetch_papers(
        self,
        search_query: str = "",
        category: str = None,
        max_results: int = None,
        sort_by: str = None,
        sort_order: str = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch papers from arXiv based on the provided parameters.

        Args:
            search_query: Search terms to filter papers
            category: arXiv category (e.g., 'cs' for Computer Science)
            max_results: Maximum number of results to return
            sort_by: Field to sort by ('submittedDate', 'relevance', etc.)
            sort_order: Order of sorting ('ascending' or 'descending')

        Returns:
            List of dictionaries containing paper information
        """
        # Use default values if parameters are not provided
        category = category if category is not None else self.default_category
        max_results = (
            max_results if max_results is not None else self.default_max_results
        )
        sort_by = sort_by if sort_by is not None else self.default_sort_by
        sort_order = sort_order if sort_order is not None else self.default_sort_order

        # Construct the search query
        search_term = self.default_search_term

        # Use provided search query if available
        if search_query:
            search_term = search_query

        # Add category if provided and search_query doesn't already specify a category
        if category and "cat:" not in search_term:
            search_term = f"cat:{category} AND {search_term}"

        params = {
            "search_query": search_term,
            "start": 0,
            "max_results": max_results,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }

        # Construct the full URL
        query_url = self.BASE_URL + urlencode(params)
        print(f"Query URL: {query_url}")

        try:
            # Fetch the feed using requests
            response = requests.get(query_url)
            print(f"Response status code: {response.status_code}")

            if response.status_code == 200:
                # Parse the response content using feedparser
                feed = feedparser.parse(response.content)
                print(f"Feed entries: {len(feed.entries)}")
            else:
                print(f"Error fetching arXiv API: {response.status_code}")
                return []
        except Exception as e:
            print(f"Exception when fetching arXiv API: {e}")
            return []

        # Process the results
        papers = []
        for entry in feed.entries:
            # Extract authors
            authors = [author.name for author in entry.authors]

            # Extract categories
            categories = [tag["term"] for tag in entry.tags] if "tags" in entry else []

            # Create a paper dictionary
            paper = {
                "title": entry.title,
                "abstract": entry.summary,
                "authors": authors,
                "published": entry.published,
                "updated": entry.updated if "updated" in entry else None,
                "link": entry.link,
                "pdf_link": next(
                    (
                        link.href
                        for link in entry.links
                        if link.rel == "alternate" and link.type == "application/pdf"
                    ),
                    None,
                ),
                "arxiv_id": entry.id.split("/abs/")[-1],
                "categories": categories,
            }

            papers.append(paper)

        return papers

    def fetch_latest_papers(
        self, category: str = None, max_results: int = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch the latest papers from arXiv in a specific category.

        Args:
            category: arXiv category (e.g., 'cs' for Computer Science)
            max_results: Maximum number of results to return

        Returns:
            List of dictionaries containing paper information
        """
        # Use default values if parameters are not provided
        category = category if category is not None else self.default_category
        max_results = (
            max_results if max_results is not None else self.default_max_results
        )

        return self.fetch_papers(category=category, max_results=max_results)

    def fetch_papers_by_subcategory(
        self, category: str = None, subcategory: str = None, max_results: int = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch papers from arXiv in a specific subcategory.

        Args:
            category: Main arXiv category (e.g., 'cs' for Computer Science)
            subcategory: arXiv subcategory (e.g., 'cs.AI' for Artificial Intelligence)
            max_results: Maximum number of results to return

        Returns:
            List of dictionaries containing paper information
        """
        # Use default values if parameters are not provided
        category = category if category is not None else self.default_category
        subcategory = (
            subcategory if subcategory is not None else self.default_subcategory
        )
        max_results = (
            max_results if max_results is not None else self.default_max_results
        )

        search_query = f"cat:{subcategory}"
        return self.fetch_papers(
            search_query=search_query, category=category, max_results=max_results
        )

    def search_papers(
        self, query: str, category: str = None, max_results: int = None
    ) -> List[Dict[str, Any]]:
        """
        Search for papers on arXiv based on a query.

        Args:
            query: Search query
            category: arXiv category (e.g., 'cs' for Computer Science)
            max_results: Maximum number of results to return

        Returns:
            List of dictionaries containing paper information
        """
        # Use default values if parameters are not provided
        category = category if category is not None else self.default_category
        max_results = (
            max_results if max_results is not None else self.default_max_results
        )

        return self.fetch_papers(
            search_query=query, category=category, max_results=max_results
        )


def format_paper_info(paper: Dict[str, Any]) -> str:
    """
    Format paper information as a readable string.

    Args:
        paper: Dictionary containing paper information

    Returns:
        Formatted string with paper information
    """
    title = paper["title"]
    authors = ", ".join(paper["authors"])
    abstract = paper["abstract"]
    published = paper["published"]
    arxiv_id = paper["arxiv_id"]

    formatted_info = f"Title: {title}\n"
    formatted_info += f"Authors: {authors}\n"
    formatted_info += f"Published: {published}\n"
    formatted_info += f"arXiv ID: {arxiv_id}\n"
    formatted_info += f"Abstract: {abstract}\n"
    formatted_info += f"Link: https://arxiv.org/abs/{arxiv_id}\n"

    return formatted_info
