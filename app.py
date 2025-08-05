"""
FastAPI application for Paperbird

This module provides a FastAPI application that serves the static HTML file
and provides API endpoints for the Paperbird application.
"""

import os
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.ai_inspector import AIInspector

from src.arxiv_fetcher import ArxivFetcher

# Create FastAPI app
app = FastAPI(
    title="Paperbird API",
    description="API for Paperbird, a tool that helps discover relevant academic papers",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory if it exists
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Create instances of our classes
arxiv_fetcher = ArxivFetcher()
ai_inspector = AIInspector()


# Define request and response models
class SearchPapersRequest(BaseModel):
    prompt: str
    timeframe: str  # "7d", "30d", "mtd", "ytd", or custom
    start_date: Optional[str] = None  # ISO format date string (YYYY-MM-DD)
    end_date: Optional[str] = None  # ISO format date string (YYYY-MM-DD)
    categories: Optional[List[str]] = None


class PaperResponse(BaseModel):
    id: str
    title: str
    authors: List[str]
    org: Optional[str] = (
        None  # Organization/institution (extracted from authors if possible)
    )
    date: str  # ISO format date string (YYYY-MM-DD)
    summary: str
    link: str
    status: str = "new"
    collected: bool = False
    notes: Optional[str] = None


@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Serve the landing page HTML."""
    with open("landingpage.html", "r") as f:
        return f.read()


@app.post("/api/search-papers", response_model=List[PaperResponse])
async def search_papers(request: SearchPapersRequest):
    """
    Search for papers based on the user's prompt and timeframe.

    This endpoint:
    1. Fetches papers from arXiv based on the timeframe
    2. Analyzes each paper for relevance based on the user's prompt
    3. Returns the relevant papers
    """
    try:
        # Calculate date range based on timeframe
        end_date = datetime.now()
        start_date = None

        if request.timeframe == "7d":
            start_date = end_date - timedelta(days=7)
        elif request.timeframe == "30d":
            start_date = end_date - timedelta(days=30)
        elif request.timeframe == "mtd":
            start_date = end_date.replace(day=1)  # First day of current month
        elif request.timeframe == "ytd":
            start_date = end_date.replace(month=1, day=1)  # First day of current year
        elif request.timeframe == "custom" and request.start_date and request.end_date:
            start_date = datetime.fromisoformat(request.start_date)
            end_date = datetime.fromisoformat(request.end_date)
        else:
            # Default to last 30 days if timeframe is invalid
            start_date = end_date - timedelta(days=30)

        # Format dates for arXiv query
        date_query = f"submittedDate:[{start_date.strftime('%Y%m%d')}000000 TO {end_date.strftime('%Y%m%d')}235959]"

        # Fetch papers from arXiv
        categories = request.categories if request.categories else ["cs.AI", "cs.LG"]
        papers = arxiv_fetcher.search_papers(
            query=date_query,
            categories=categories,
            max_results=50,  # Limit to 50 papers for performance
        )

        # Analyze papers for relevance
        relevant_papers = []
        for paper in papers:
            analysis = ai_inspector.analyze_paper(paper, request.prompt)

            if analysis["is_relevant"]:
                # Extract organization from authors if possible
                org = None
                if paper.get("authors") and len(paper["authors"]) > 0:
                    # Try to extract organization from the first author
                    # This is a simplification - in reality, you'd want a more sophisticated approach
                    author_parts = paper["authors"][0].split()
                    if len(author_parts) > 1:
                        org = author_parts[-1]

                # Format the paper for the response
                relevant_paper = PaperResponse(
                    id=paper.get("arxiv_id", ""),
                    title=paper.get("title", ""),
                    authors=paper.get("authors", []),
                    org=org,
                    date=datetime.strptime(
                        paper.get("published", ""), "%Y-%m-%dT%H:%M:%SZ"
                    ).strftime("%Y-%m-%d"),
                    summary=analysis.get("summary", ""),
                    link=paper.get("link", ""),
                    status="new",
                    collected=False,
                    notes=None,
                )
                relevant_papers.append(relevant_paper)

        return relevant_papers

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching papers: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
