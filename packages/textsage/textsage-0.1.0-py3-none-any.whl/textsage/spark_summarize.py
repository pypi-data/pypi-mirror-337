from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

from .setup_ollama import ensure_ollama_setup
from .summarize import summarize_text


def summarize_spark_dataframe(df, text_column, model_name="mistral", word_count=10):
    """
    Summarize the contents of a specified text column in a
    Spark DataFrame using Ollama.

    Args:
        df (pyspark.sql.DataFrame): The Spark DataFrame containing the text data.
        text_column (str): The name of the column to summarize.
        model_name (str): The name of the model to use for summarization.
                          Default is 'mistral'.
        word_count (int): The maximum number of words for the summary.
                          Default is 10.

    Raises:
        ValueError: If the specified text column does not exist or is not of type string.

    Example:
        from pyspark.sql import SparkSession
        spark = SparkSession.builder.getOrCreate()
        data = [("This is a long text that needs summarization.",)]
        df = spark.createDataFrame(data, ["Text"])
        summarized_df = summarize_spark_dataframe(df, 'Text', 'mistral', 20)
        summarized_df.show()

    Returns:
        pyspark.sql.DataFrame: A new DataFrame with the original text and its summary.
    """

    ensure_ollama_setup(model_name)

    # Check if column exists
    if text_column not in df.columns:
        raise ValueError(f"Column '{text_column}' does not exist in the DataFrame.")

    # Check if column is string type
    if df.schema[text_column].dataType != StringType():
        raise ValueError(f"Column '{text_column}' must be of type string.")

    # Define UDF for text summarization
    summarize_udf = udf(lambda text: summarize_text(text, model_name, word_count), StringType())

    # Apply the summarization UDF to create new column
    result_df = df.withColumn(f"crux_{text_column}", summarize_udf(df[text_column]))

    return result_df
