"""
Test script for the AIInspector module.

This script demonstrates how to use the AIInspector module to analyze a paper
and determine its relevance to a user's interests.
"""

import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from src.ai_inspector import AIInspector


def main():
    """
    Main function to demonstrate the AIInspector module.
    """
    print("Testing the AIInspector module...")

    # Create a sample paper dictionary
    sample_paper = {
        "title": "Deep Learning-Based Recommendation Systems: A Comprehensive Survey",
        "abstract": """
        Recommendation systems play a crucial role in various online platforms by suggesting relevant items to users.
        With the advancement of deep learning techniques, recommendation systems have evolved significantly.
        This paper provides a comprehensive survey of deep learning-based recommendation systems, covering various
        architectures, algorithms, and evaluation metrics. We discuss the challenges and future directions in this field,
        including handling sparse data, cold-start problems, and improving recommendation diversity.
        """,
        "authors": ["Jane Smith", "John Doe", "Alice Johnson"],
        "categories": ["cs.IR", "cs.AI", "cs.LG"],
        "arxiv_id": "2301.12345",
        "published": "2023-01-15T12:00:00Z",
        "link": "https://arxiv.org/abs/2301.12345",
    }

    # Define a sample user prompt
    user_prompt = """
    I am a Product Manager working on AI-powered recommendation systems for e-commerce.
    I'm interested in the latest research on personalization algorithms, user behavior modeling,
    and techniques to improve recommendation accuracy and diversity.
    I'm particularly focused on methods that can work with sparse data and cold-start problems.
    My company competes with Amazon, Alibaba, and other major e-commerce platforms.
    """

    print("\nSample Paper:")
    print(f"Title: {sample_paper['title']}")
    print(f"Authors: {', '.join(sample_paper['authors'])}")
    print(f"Categories: {', '.join(sample_paper['categories'])}")
    print(f"Abstract: {sample_paper['abstract'].strip()}")
    print()

    print("Sample User Prompt:")
    print(user_prompt.strip())
    print()

    # Create an instance of AIInspector
    inspector = AIInspector(temperature=0.7, max_tokens=500)
    print("AIInspector initialized.")
    print()

    # Check if the paper is relevant
    print("Checking paper relevance...")
    is_relevant, reason = inspector.check_relevance(sample_paper, user_prompt)
    print(f"Is Relevant: {is_relevant}")
    print(f"Reason: {reason}")
    print()

    # Generate a summary if the paper is relevant
    if is_relevant:
        print("Generating paper summary...")
        summary = inspector.generate_summary(sample_paper, user_prompt)
        print("Summary:")
        print(summary)
    else:
        print("Paper is not relevant. No summary generated.")
    print()

    # Analyze the paper (combines relevance check and summary generation)
    print("Analyzing paper...")
    analysis = inspector.analyze_paper(sample_paper, user_prompt)
    print("Analysis Results:")
    print(f"Paper ID: {analysis['paper_id']}")
    print(f"Title: {analysis['title']}")
    print(f"Is Relevant: {analysis['is_relevant']}")
    print(f"Relevance Reason: {analysis['relevance_reason']}")

    if analysis["is_relevant"] and "summary" in analysis:
        print("Summary:")
        print(analysis["summary"])


if __name__ == "__main__":
    main()
