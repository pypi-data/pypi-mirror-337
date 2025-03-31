import pandas as pd

from .setup_ollama import ensure_ollama_setup
from .llm_utils import summarize_text, analyze_sentiment, extract_key_phrases


def transform_dataframe(df, text_column, model_name="mistral", word_count=50, summarize=True, sentiment=False, key_phrases=False):
    """
    Transform the contents of a specified text column in a
    pandas DataFrame by applying summarization, sentiment analysis,
    and/or key phrase extraction.

    Args:
        df (pd.DataFrame): The DataFrame containing the text data.
        text_column (str): The name of the column to process.
        model_name (str): The name of the model to use for processing.
                          Default is 'mistral'.
        word_count (int): The maximum number of words for the summary.
                          Default is 50.
        summarize (bool): Whether to summarize the text. Default is True.
        sentiment (bool): Whether to analyze sentiment of the text. Default is False.
        key_phrases (bool): Whether to extract key phrases from the text. Default is False.

    Raises:
        ValueError: If the specified text column does not exist or is not of type string.

    Example:
        df = pd.DataFrame({'Text': ["This is a long text that needs summarization."]})
        transformed_df = transform_dataframe(df, 'Text', 'mistral', summarize=True, sentiment=True, key_phrases=True)
        print(transformed_df)

    Returns:
        pd.DataFrame: A new DataFrame with the original text and additional columns
                      for summaries, sentiment analysis, and/or key phrases as specified.
    """

    ensure_ollama_setup(model_name)

    # Ensure the text column exists
    if text_column not in df.columns:
        raise ValueError(f"Column '{text_column}' does not exist in the DataFrame.")
    # Ensure the text column is of type string
    if not pd.api.types.is_string_dtype(df[text_column]):
        raise ValueError(f"Column '{text_column}' must be of type string.")

    if summarize:
        df[f"summarize_{text_column}"] = df[text_column].apply(
            lambda text: summarize_text(text, model_name, word_count, check_ollama_setup=False)
        )
    if sentiment:
        df[f"sentiment_{text_column}"] = df[text_column].apply(
            lambda text: analyze_sentiment(text, model_name, check_ollama_setup=False)
        )
    if key_phrases:
        df[f"key_phrases_{text_column}"] = df[text_column].apply(
            lambda text: extract_key_phrases(text, model_name, check_ollama_setup=False)
        )

    return df
