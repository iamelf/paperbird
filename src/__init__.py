"""
Paperbird package initialization.

This package contains modules for fetching and processing arXiv papers.
"""

from .arxiv_fetcher import ArxivFetcher, format_paper_info

__all__ = ["ArxivFetcher", "format_paper_info"]
