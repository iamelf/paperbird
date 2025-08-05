"""
AI Inspector Module

This module takes information about a paper, feeds it to a Llama model with a prompt,
and parses the response from the Llama model.
"""

import json
from typing import Any, Dict, Optional, Tuple, Union

import requests


class AIInspector:
    """
    A class to interact with Llama model for paper analysis.
    """

    # Hardcoded API token for now
    API_TOKEN = "LLM|1207785234387418|nSRelSUWRp1aGGAatZbbtHXHNSM"
    API_URL = "https://api.llama.com/v1/chat/completions"  # Example URL, replace with actual Llama API endpoint

    def __init__(self, temperature: float = 0.7, max_tokens: int = 500):
        """
        Initialize the AIInspector with default parameters.

        Args:
            temperature: Controls randomness in the response (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate in the response
        """
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.headers = {
            "Authorization": f"Bearer {self.API_TOKEN}",
            "Content-Type": "application/json",
        }

    def _call_llama_api(self, prompt: str) -> Dict[str, Any]:
        """
        Make a call to the Llama API with the given prompt.

        Args:
            prompt: The prompt to send to the Llama model

        Returns:
            The JSON response from the Llama API

        Raises:
            Exception: If the API call fails
        """
        payload = {
            "model": "Llama-4-Maverick-17B-128E-Instruct-FP8",  # Correct model name from curl command
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        try:
            response = requests.post(self.API_URL, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error calling Llama API: {e}")

    def check_relevance(
        self, paper: Dict[str, Any], user_prompt: str
    ) -> Tuple[bool, str]:
        """
        Check if a paper is relevant to a user's interests based on their prompt.

        Args:
            paper: Dictionary containing paper information
            user_prompt: The user's relevance prompt describing their interests

        Returns:
            A tuple containing (is_relevant, reason)
        """
        # Extract paper information
        title = paper.get("title", "")
        abstract = paper.get("abstract", "")
        authors = ", ".join(paper.get("authors", []))
        categories = ", ".join(paper.get("categories", []))

        # Construct the prompt for the Llama model
        prompt = f"""
        You are an AI assistant helping to determine if an academic paper is relevant to a user's interests.

        USER'S INTERESTS:
        {user_prompt}

        PAPER INFORMATION:
        Title: {title}
        Authors: {authors}
        Categories: {categories}
        Abstract: {abstract}

        Based on the user's interests and the paper information, determine if this paper is relevant to the user.
        Return your response as a JSON object with the following format:
        {{
            "is_relevant": true/false,
            "reason": "A brief explanation of why the paper is or is not relevant"
        }}
        """

        # Call the Llama API
        try:
            response = self._call_llama_api(prompt)

            # Parse the response based on the format from the curl command
            response_text = (
                response.get("completion_message", {})
                .get("content", {})
                .get("text", "")
                .strip()
            )

            # Find the JSON object in the response
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1

            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                result = json.loads(json_str)
                return result.get("is_relevant", False), result.get(
                    "reason", "No reason provided"
                )
            else:
                return False, "Failed to parse response from AI model"

        except Exception as e:
            return False, f"Error processing relevance check: {e}"

    def generate_summary(self, paper: Dict[str, Any], user_prompt: str) -> str:
        """
        Generate a summary of a paper tailored to the user's interests.

        Args:
            paper: Dictionary containing paper information
            user_prompt: The user's relevance prompt describing their interests

        Returns:
            A summary of the paper tailored to the user's interests
        """
        # Extract paper information
        title = paper.get("title", "")
        abstract = paper.get("abstract", "")
        authors = ", ".join(paper.get("authors", []))
        categories = ", ".join(paper.get("categories", []))

        # Construct the prompt for the Llama model
        prompt = f"""
        You are an AI assistant helping to summarize an academic paper based on a user's interests.

        USER'S INTERESTS:
        {user_prompt}

        PAPER INFORMATION:
        Title: {title}
        Authors: {authors}
        Categories: {categories}
        Abstract: {abstract}

        Generate a concise summary (100-150 words) of this paper that highlights aspects most relevant to the user's interests.
        Focus on practical implications, potential applications, and how this research might impact the user's work.
        """

        # Call the Llama API
        try:
            response = self._call_llama_api(prompt)

            # Extract the summary from the response based on the format from the curl command
            summary = (
                response.get("completion_message", {})
                .get("content", {})
                .get("text", "")
                .strip()
            )
            return summary

        except Exception as e:
            return f"Error generating summary: {e}"

    def analyze_paper(self, paper: Dict[str, Any], user_prompt: str) -> Dict[str, Any]:
        """
        Analyze a paper for relevance and generate a summary if relevant.

        Args:
            paper: Dictionary containing paper information
            user_prompt: The user's relevance prompt describing their interests

        Returns:
            A dictionary containing the analysis results
        """
        # Check if the paper is relevant
        is_relevant, reason = self.check_relevance(paper, user_prompt)

        result = {
            "paper_id": paper.get("arxiv_id", ""),
            "title": paper.get("title", ""),
            "is_relevant": is_relevant,
            "relevance_reason": reason,
        }

        # If the paper is relevant, generate a summary
        if is_relevant:
            summary = self.generate_summary(paper, user_prompt)
            result["summary"] = summary

        return result
