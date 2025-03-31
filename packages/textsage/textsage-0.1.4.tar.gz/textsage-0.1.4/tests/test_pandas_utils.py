import unittest
import pandas as pd
from textsage.pandas_utils import transform_dataframe


class TestPandasSummarize(unittest.TestCase):
    def setUp(self):
        # Create a sample DataFrame for testing
        self.df = pd.DataFrame({
            'text': ['Ollama allows running local LLMs efficiently.',
                    'Python is a versatile programming language.']
        })

    def test_summarize_dataframe(self):
        # Test basic summarization
        result_df = transform_dataframe(self.df, 'text', 'mistral', summarize=True, sentiment=True, key_phrases=True)
        
        # Check if the new columns are added
        self.assertIn('summarize_text', result_df.columns)
        self.assertIn('sentiment_text', result_df.columns)
        self.assertIn('key_phrases_text', result_df.columns)
        
        # Check if the number of rows is unchanged
        self.assertEqual(len(result_df), len(self.df))
        self.assertTrue(all(isinstance(x, str) for x in result_df['summarize_text']))
        self.assertTrue(all(isinstance(x, dict) for x in result_df['sentiment_text']))
        self.assertTrue(all(isinstance(x, list) for x in result_df['key_phrases_text']))

    def test_invalid_column(self):
        # Test with non-existent column
        with self.assertRaises(ValueError):
            transform_dataframe(self.df, 'invalid_column')

    def test_non_string_column(self):
        # Test with non-string column
        df_invalid = pd.DataFrame({'numbers': [1, 2, 3]})
        with self.assertRaises(ValueError):
            transform_dataframe(df_invalid, 'numbers')


if __name__ == '__main__':
    unittest.main()
