# TextSage

TextSage is a Python library that sets up Ollama and local LLMs for users and provides simple functions to summarize text, with support for Python, Pandas, and PySpark workflows.

## Features

- Automated Ollama Setup:

  - Checks if Ollama is installed and running
  - Installs Ollama if not found
  - Downloads specified LLM models for summarization

- Multiple Integration Options:
  - Pure Python text summarization
  - Pandas DataFrame column summarization
  - PySpark DataFrame column summarization

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

### Basic Text Summarization

```python
from textsage import summarize_text

text = "This is a long text that needs summarization."
summary = summarize_text(text, model_name="mistral", word_count=10)
print(summary)
```

### Pandas DataFrame Summarization

```python
import pandas as pd
from textsage import summarize_dataframe

# Create a sample DataFrame
df = pd.DataFrame({
    'text': ['This is a long text that needs summarization.']
})

# Summarize the 'text' column
result_df = summarize_dataframe(df, 'text', model_name='mistral')
print(result_df['summary'])
```

### PySpark DataFrame Summarization

```python
from pyspark.sql import SparkSession
from textsage import summarize_spark_dataframe

# Create a Spark session
spark = SparkSession.builder.getOrCreate()

# Create a sample DataFrame
data = [("This is a long text that needs summarization.",)]
spark_df = spark.createDataFrame(data, ["text"])

# Summarize the 'text' column
result_df = summarize_spark_dataframe(spark_df, 'text', model_name='mistral')
result_df.show()
```

## Supported Models

By default, textsage uses the 'mistral' model, but you can specify any model supported by Ollama:

- mistral
- llama2
- codellama
- phi
- neural-chat
- And more...

## Requirements

- Python 3.8+
- Ollama (automatically installed if missing)
- pandas (optional, for DataFrame support)
- pyspark (optional, for Spark support)

## License

This project is licensed under the MIT License.
