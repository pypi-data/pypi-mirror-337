import ollama
from typing import Dict, List
import json
from .setup_ollama import ensure_ollama_setup

def summarize_text(text, model_name: str = "mistral", word_count: int = 50, check_ollama_setup: bool = True) -> str:
    """Summarize the given text using Ollama's local LLM.
    Args:
        text (str): The text to summarize.
        model_name (str): The name of the model to use for summarization.
        word_count (int): The maximum number of words for the summary.
        check_ollama_setup (bool): Whether to check and set up Ollama before use.

    Raises:
        ValueError: If the model name is not provided.
    Example:
        text = "This is a long text that needs summarization."
        model_name = "mistral"
        summary = summarize_text(text, model_name, word_count)
        print(summary)
    Returns:
        str: The summarized text.

    """
    if check_ollama_setup:
        ensure_ollama_setup(model_name)
    
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that summarizes text concisely.",
        },
        {
            "role": "user",
            "content": f"Summarize the following text in less than {word_count} words:\n\n{text}",
        },
    ]

    try:
        response = ollama.chat(model=model_name, messages=messages)
        return response["message"]["content"].strip()
    except Exception as e:
        return f"Error while summarizing: {e}"

def analyze_sentiment(text: str, model_name: str = "mistral", check_ollama_setup: bool = True) -> Dict[str, float]:
    """Analyze sentiment scores for the given text.
    
    Args:
        text (str): Text to analyze
        model_name (str): Name of the LLM model to use
        check_ollama_setup (bool): Whether to check and set up Ollama before use.
        
    Returns:
        Dict[str, float]: Dictionary containing sentiment scores
    """
    if check_ollama_setup:
        ensure_ollama_setup(model_name)
    
    messages = [
        {
            "role": "system",
            "content": "You are a sentiment analysis expert. Provide sentiment scores as JSON.",
        },
        {
            "role": "user",
            "content": f"Analyze the sentiment of this text and return only numerical scores for positive, negative, and neutral emotions (values between 0-1, sum to 1). Respond using JSON format:\n\n{text}",
        },
    ]
    
    try:
        response = ollama.chat(model=model_name, messages=messages, format="json")
        scores = json.loads(response["message"]["content"])
        return scores
    except Exception as e:
        return {"error": str(e)}

def extract_key_phrases(text: str, model_name: str = "mistral",num_phrases: int = 5, check_ollama_setup: bool = True) -> List[str]:
    """Extract key phrases from the text.
    
    Args:
        text (str): Text to analyze
        model_name (str): Name of the LLM model to use
        num_phrases (int): Number of key phrases to extract
        check_ollama_setup (bool): Whether to check and set up Ollama before use.
        
    Returns:
        List[str]: List of key phrases
    """
    if check_ollama_setup:
        ensure_ollama_setup(model_name)
    
    messages = [
        {
            "role": "system",
            "content": "You are an expert at extracting key phrases from text.",
        },
        {
            "role": "user",
            "content": f"Extract exactly {num_phrases} key phrases from this text. Return only the phrases, one per line:\n\n{text}",
        },
    ]
    
    try:
        response = ollama.chat(model=model_name, messages=messages)
        phrases = response["message"]["content"].strip().split("\n")
        return phrases[:num_phrases]
    except Exception as e:
        return [f"Error: {str(e)}"]
