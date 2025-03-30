import ollama


def summarize_text(text, model_name, word_count=50):
    """Summarize the given text using Ollama's local LLM.
    Args:
        text (str): The text to summarize.
        model_name (str): The name of the model to use for summarization.
        word_count (int): The maximum number of words for the summary.

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
