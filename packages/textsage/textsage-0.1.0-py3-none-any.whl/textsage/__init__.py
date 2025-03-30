from .pandas_summarize import summarize_pandas_dataframe
from .spark_summarize import summarize_spark_dataframe
from .summarize import summarize_text

"""
textsage is a Python library that sets up Ollama and local LLMs for users and provides a simple function to summarize text.

Author: Shivang Agarwal
License: MIT
"""

__version__ = "0.1.0"
__author__ = "Shivang Agarwal"
__license__ = "MIT"

__all__ = [
    "summarize_text",
    "summarize_pandas_dataframe",
    "summarize_spark_dataframe",
]
