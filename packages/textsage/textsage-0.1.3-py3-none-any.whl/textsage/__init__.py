"""
TextSage is a Python library that sets up Ollama and local LLMs for users and 
provides a simple function to summarize text.
"""

from .pandas_summarize import summarize_pandas_dataframe
from .summarize import summarize_text

__all__ = [
    "summarize_text",
    "summarize_pandas_dataframe",
]
