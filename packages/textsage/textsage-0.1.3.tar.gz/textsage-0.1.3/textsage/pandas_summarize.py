import pandas as pd

from .setup_ollama import ensure_ollama_setup
from .summarize import summarize_text


def summarize_pandas_dataframe(df, text_column, model_name="mistral", word_count=10):
    """
    Summarize the contents of a specified text column in a
    pandas DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the text data.
        text_column (str): The name of the column to summarize.
        model_name (str): The name of the model to use for summarization.
                          Default is 'mistral'.
        word_count (int): The maximum number of words for the summary.
                          Default is 10.

    Raises:
        ValueError: If the specified text column does not exist or is not of type string.

    Example:
        df = pd.DataFrame({'Text': ["This is a long text that needs summarization."]})
        summarized_df = summarize_pandas_dataframe(df, 'Text', 'mistral')
        print(summarized_df)

    Returns:
        pd.DataFrame: A new DataFrame with the original text and its summary.
    """

    ensure_ollama_setup(model_name)

    # Ensure the text column exists
    if text_column not in df.columns:
        raise ValueError(f"Column '{text_column}' does not exist in the DataFrame.")
    # Ensure the text column is of type string
    if not pd.api.types.is_string_dtype(df[text_column]):
        raise ValueError(f"Column '{text_column}' must be of type string.")

    df[f"summarize_{text_column}"] = df[text_column].apply(
        lambda text: summarize_text(text, model_name, word_count)
    )

    return df
