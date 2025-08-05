"""
Paperbird package initialization.

This package contains modules for fetching, processing, and analyzing arXiv papers.
"""

from .ai_inspector import AIInspector
from .arxiv_fetcher import ArxivFetcher, format_paper_info

__all__ = ["ArxivFetcher", "format_paper_info", "AIInspector"]
