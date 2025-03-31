"""
TextSage is a Python library that sets up Ollama and local LLMs for users and 
provides a simple function to summarize text.
"""

from .llm_utils import summarize_text, analyze_sentiment, extract_key_phrases

__all__ = [
    "summarize_text",
    "analyze_sentiment",
    "extract_key_phrases"
]
