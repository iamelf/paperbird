"""
Script to fetch and display arXiv papers.

This script demonstrates the use of the ArxivFetcher module.
"""

from src.arxiv_fetcher import ArxivFetcher, format_paper_info


def main():
    """
    Main function to fetch and display arXiv papers.
    """
    print("Paperbird - ArXiv Paper Fetcher")
    print("===============================\n")

    print("Fetching latest papers from arXiv...")

    # Create an instance of ArxivFetcher
    fetcher = ArxivFetcher()

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
