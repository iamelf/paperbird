"""
Main script to demonstrate the ArxivFetcher and AIInspector modules.

This script fetches the latest papers from arXiv, analyzes them using the AIInspector,
and displays their information along with relevance and summaries.
"""

import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from src.ai_inspector import AIInspector

# Import the required classes from the src package
from src.arxiv_fetcher import ArxivFetcher, format_paper_info


def main():
    """
    Main function to demonstrate the ArxivFetcher and AIInspector modules.
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

    # Create an instance of AIInspector
    inspector = AIInspector(temperature=0.7, max_tokens=500)
    print("AIInspector initialized.")
    print()

    # Define a sample user prompt
    user_prompt = """
    I am a Product Manager working on AI-powered recommendation systems for e-commerce.
    I'm interested in the latest research on personalization algorithms, user behavior modeling,
    and techniques to improve recommendation accuracy and diversity.
    I'm particularly focused on methods that can work with sparse data and cold-start problems.
    My company competes with Amazon, Alibaba, and other major e-commerce platforms.
    """

    print("Sample user prompt defined:")
    print(user_prompt)
    print()

    # Fetch papers by category
    print("\nFetching papers from the AI and ML category...")
    category_papers = fetcher.search_papers(
        query="all:recommender system",
        categories=["cs.AI", "cs.LG"],  # AI and Machine Learning categories
        max_results=5,  # Reduced for demonstration purposes
    )

    print(f"Found {len(category_papers)} papers in AI and ML category.\n")

    # Analyze each paper using the AIInspector
    print("Analyzing papers for relevance to the user prompt...")
    for i, paper in enumerate(category_papers, 1):
        print(f"\nPaper {i}: {paper['title']}")

        # Analyze the paper
        analysis = inspector.analyze_paper(paper, user_prompt)

        # Display relevance information
        print(f"Relevant: {analysis['is_relevant']}")
        print(f"Reason: {analysis['relevance_reason']}")

        # If relevant, display the summary
        if analysis["is_relevant"]:
            print("\nSummary:")
            print(analysis.get("summary", "No summary generated."))

        print("-" * 80)  # Separator


if __name__ == "__main__":
    main()
