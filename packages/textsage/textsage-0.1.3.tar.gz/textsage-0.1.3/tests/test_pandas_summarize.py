import unittest
import pandas as pd
from textsage.pandas_summarize import summarize_pandas_dataframe


class TestPandasSummarize(unittest.TestCase):
    def setUp(self):
        # Create a sample DataFrame for testing
        self.df = pd.DataFrame({
            'text': ['Ollama allows running local LLMs efficiently.',
                    'Python is a versatile programming language.']
        })

    def test_summarize_dataframe(self):
        # Test basic summarization
        result_df = summarize_pandas_dataframe(self.df, 'text', 'mistral')
        self.assertIn('summarize_text', result_df.columns)
        self.assertEqual(len(result_df), len(self.df))
        self.assertTrue(all(isinstance(x, str) for x in result_df['summarize_text']))

    def test_invalid_column(self):
        # Test with non-existent column
        with self.assertRaises(ValueError):
            summarize_pandas_dataframe(self.df, 'invalid_column')

    def test_non_string_column(self):
        # Test with non-string column
        df_invalid = pd.DataFrame({'numbers': [1, 2, 3]})
        with self.assertRaises(ValueError):
            summarize_pandas_dataframe(df_invalid, 'numbers')


if __name__ == '__main__':
    unittest.main()
