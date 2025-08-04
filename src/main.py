"""
Main script to demonstrate the ArxivFetcher module.

This script fetches the latest papers from arXiv and displays their information.
"""

import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Import the ArxivFetcher class from the src package
from src.arxiv_fetcher import ArxivFetcher, format_paper_info


def main():
    """
    Main function to demonstrate the ArxivFetcher module.
    """
    print("Fetching latest papers from arXiv...")

    # Create an instance of ArxivFetcher with custom default values
    fetcher = ArxivFetcher(
        default_search_term="all:recommendation",
        default_category=None,  # No category restriction to get more results
        default_subcategory="cs.AI",  # Artificial Intelligence subcategory
        default_max_results=10,
        default_sort_by="submittedDate",
        default_sort_order="descending",
    )

    print("ArxivFetcher initialized with the following default values:")
    print(f"- Default search term: {fetcher.default_search_term}")
    print(f"- Default category: {fetcher.default_category}")
    print(f"- Default subcategory: {fetcher.default_subcategory}")
    print(f"- Default max results: {fetcher.default_max_results}")
    print(f"- Default sort by: {fetcher.default_sort_by}")
    print(f"- Default sort order: {fetcher.default_sort_order}")
    print()

    # Fetch the latest papers in Computer Science (default category)
    # Limiting to 5 papers for demonstration purposes
    papers = fetcher.fetch_latest_papers(max_results=5)

    print(f"Found {len(papers)} papers.\n")

    # Display information for each paper
    for i, paper in enumerate(papers, 1):
        print(f"Paper {i}:")
        print(format_paper_info(paper))
        print("-" * 80)  # Separator

    # Example of searching for papers with a specific query
    print("\nSearching for papers related to 'large language models'...")
    search_papers = fetcher.search_papers(
        query="all:large language models", max_results=3
    )

    print(f"Found {len(search_papers)} papers.\n")

    # Display information for each search result
    for i, paper in enumerate(search_papers, 1):
        print(f"Search Result {i}:")
        print(format_paper_info(paper))
        print("-" * 80)  # Separator


if __name__ == "__main__":
    main()
