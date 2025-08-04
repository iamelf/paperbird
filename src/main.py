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
        default_search_term="all:recommendation system",
        default_categories=["cs.AI", "cs.LG"],  # AI and Machine Learning categories
        default_max_results=10,
        default_sort_by="submittedDate",
        default_sort_order="descending",
    )

    print("ArxivFetcher initialized with the following default values:")
    print(f"- Default search term: {fetcher.default_search_term}")
    print(f"- Default categories: {fetcher.default_categories}")
    print(f"- Default max results: {fetcher.default_max_results}")
    print(f"- Default sort by: {fetcher.default_sort_by}")
    print(f"- Default sort order: {fetcher.default_sort_order}")
    print()

    # Fetch papers by category
    print("\nFetching papers from the AI and ML category...")
    category_papers = fetcher.search_papers(
        query="all:recommender system",
        categories=["cs.AI", "cs.LG"],  # Computation and Language category
        max_results=10,
    )

    print(f"Found {len(category_papers)} papers in AI and ML category.\n")

    # Display information for each paper in the category
    for i, paper in enumerate(category_papers, 1):
        print(f"Category Paper {i}:")
        print(format_paper_info(paper))
        print("-" * 80)  # Separator


if __name__ == "__main__":
    main()
