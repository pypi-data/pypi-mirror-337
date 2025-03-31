from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

from .setup_ollama import ensure_ollama_setup
from .llm_utils import summarize_text, analyze_sentiment, extract_key_phrases


def transform_dataframe(df, text_column, model_name="mistral", word_count=50, summarize=True, sentiment=False, key_phrases=False):
    """
    Transform the contents of a specified text column in a
    Spark DataFrame using Ollama. This includes options for summarization,
    sentiment analysis, and key phrase extraction.

    Args:
        df (pyspark.sql.DataFrame): The Spark DataFrame containing the text data.
        text_column (str): The name of the column to process.
        model_name (str): The name of the model to use for processing.
                          Default is 'mistral'.
        word_count (int): The maximum number of words for the summary.
                          Default is 50.
        summarize (bool): Whether to summarize the text. Default is True.
        sentiment (bool): Whether to analyze sentiment. Default is False.
        key_phrases (bool): Whether to extract key phrases. Default is False.

    Raises:
        ValueError: If the specified text column does not exist or is not of type string.

    Example:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.getOrCreate()
        data = [("This is a long text that needs summarization.",)]
        df = spark.createDataFrame(data, ["Text"])
        transformed_df = transform_dataframe(df, 'Text', 'mistral', 20, summarize=True, sentiment=True, key_phrases=True)
        transformed_df.show()

    Returns:
        pyspark.sql.DataFrame: A new DataFrame with the original text and the requested transformations.
    """

    ensure_ollama_setup(model_name)

    # Check if column exists
    if text_column not in df.columns:
        raise ValueError(f"Column '{text_column}' does not exist in the DataFrame.")

    # Check if column is string type
    if df.schema[text_column].dataType != StringType():
        raise ValueError(f"Column '{text_column}' must be of type string.")

    if summarize:
        # Define UDF for text summarization
        summarize_udf = udf(
            lambda text: summarize_text(text, model_name, word_count, check_ollama_setup=False), StringType()
        )
        df = df.withColumn(f"summarize_{text_column}", summarize_udf(df[text_column]))

    if sentiment:
        # Define UDF for sentiment analysis
        sentiment_udf = udf(
            lambda text: analyze_sentiment(text, model_name, check_ollama_setup=False), StringType()
        )
        df = df.withColumn(f"sentiment_{text_column}", sentiment_udf(df[text_column]))
    if key_phrases:
        # Define UDF for key phrase extraction
        key_phrases_udf = udf(
            lambda text: extract_key_phrases(text, model_name, check_ollama_setup=False), StringType()
        )
        df = df.withColumn(f"key_phrases_{text_column}", key_phrases_udf(df[text_column]))

    return df
