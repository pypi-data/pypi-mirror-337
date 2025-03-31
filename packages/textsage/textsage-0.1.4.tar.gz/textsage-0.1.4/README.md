# TextSage

TextSage is a Python library designed to securely set up and utilize Ollama and local LLMs for text analysis. It ensures that all processing happens locally on your machine, making it an ideal solution for handling sensitive or confidential data. With support for Python, Pandas, and PySpark workflows, TextSage provides a seamless and secure way to analyze text without compromising data privacy.

## Features

- Automated Ollama Setup:

  - Checks if Ollama is installed and running
  - Installs Ollama if not found
  - Downloads specified LLM models

- Text Analysis Capabilities:

  - Text summarization
  - Sentiment analysis
  - Key phrase extraction

- Multiple Integration Options:
  - Pure Python text processing
  - Pandas DataFrame processing
  - PySpark DataFrame processing

## Installation

```bash
pip install textsage
```

## Dependency

`textsage` uses Ollama to host a local LLM on your machine and perform summarization tasks. If Ollama is not already installed, the `textsage` package will attempt to install it on macOS and Linux using following commands.

```bash
# macOS (Please ensure Homebrew is installed on macOS)
brew install --cask ollama
```

```bash
# linux
curl -fsSL https://ollama.com/install.sh | sh
```

For Windows, please download Ollama directly from [here](https://ollama.com/download/windows).

The default quantized Mistral model (~4GB) will be downloaded and used for summarization. Ensure sufficient RAM is available for hosting the local LLM.

> Note: Ollama and LLM installation is a one-time setup. Once installed, TextSage can be used directly without reinstallation.

## Usage

### Basic Text Analysis

```python
from textsage import summarize_text, analyze_sentiment, extract_key_phrases

text = "This is a sample text that needs analysis."

# Get summary
summary = summarize_text(text, model_name="mistral", word_count=10)
print(summary)

# Analyze sentiment
sentiment = analyze_sentiment(text, model_name="mistral")
print(sentiment)  # Returns: {"positive": 0.7, "negative": 0.1, "neutral": 0.2}

# Extract key phrases
phrases = extract_key_phrases(text, model_name="mistral", num_phrases=5)
print(phrases)  # Returns list of key phrases
```

### Pandas DataFrame Summarization

```python
import pandas as pd
from textsage import summarize_dataframe

# Create a sample DataFrame
df = pd.DataFrame({
    'column_1': ['This is a long text that needs summarization.']
})

# Summarize the 'text' column
result_df = summarize_dataframe(df, text_column='column_1', model_name='mistral')
print(result_df['summary'])
```

### Pandas DataFrame Transformation

```python
import pandas as pd
from textsage.pandas_utils import transform_dataframe

# Create a sample DataFrame
df = pd.DataFrame({
    'text': ['This is a text that needs analysis.']
})

# Process the text column
result_df = transform_dataframe(
    df,
    'text',
    model_name='mistral',
    summarize=True,
    sentiment=True,
    key_phrases=True
)
```

### PySpark DataFrame Summarization

```python
from pyspark.sql import SparkSession
from textsage import summarize_spark_dataframe

# Create a Spark session
spark = SparkSession.builder.getOrCreate()

# Create a sample DataFrame
data = [("This is a long text that needs summarization.",)]
spark_df = spark.createDataFrame(data, ["column_1"])

# Summarize the 'text' column
result_df = summarize_spark_dataframe(spark_df, text_column='column_1', model_name='mistral')
result_df.show()
```

### PySpark DataFrame Transformation

```python
from pyspark.sql import SparkSession
from textsage.spark_utils import transform_dataframe

# Create a Spark session
spark = SparkSession.builder.getOrCreate()

# Create a sample DataFrame
data = [("This is a text that needs analysis.",)]
spark_df = spark.createDataFrame(data, ["text"])

# Process the text column
result_df = transform_dataframe(
    spark_df,
    'text',
    model_name='mistral',
    summarize=True,
    sentiment=True,
    key_phrases=True
)
```

## Supported Models

By default, textsage uses the 'mistral' model, but you can specify any model supported by Ollama:

- mistral
- llama3.2
- deepseek-r1
- phi
- And more...

## Requirements

- Python 3.8+
- Ollama (automatically installed if missing)
- pandas (optional, for DataFrame support)
- pyspark (optional, for Spark support)

## License

This project is licensed under the MIT License.
