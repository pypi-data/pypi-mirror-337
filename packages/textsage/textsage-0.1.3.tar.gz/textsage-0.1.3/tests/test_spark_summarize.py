import unittest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from textsage.spark_summarize import summarize_spark_dataframe


class TestSparkSummarize(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create Spark session
        cls.spark = SparkSession.builder \
            .appName("test_summarize") \
            .master("local[1]") \
            .getOrCreate()
        
        # Create sample data
        data = [("Ollama allows running local LLMs efficiently.",),
                ("Python is a versatile programming language.",)]
        cls.df = cls.spark.createDataFrame(data, ["text"])

    def test_summarize_dataframe(self):
        # Test basic summarization
        result_df = summarize_spark_dataframe(self.df, 'text', 'mistral')
        self.assertIn('summarize_text', result_df.columns)
        self.assertEqual(result_df.count(), self.df.count())

    def test_invalid_column(self):
        # Test with non-existent column
        with self.assertRaises(ValueError):
            summarize_spark_dataframe(self.df, 'invalid_column')

    def test_non_string_column(self):
        # Test with non-string column
        schema = StructType([StructField("numbers", IntegerType(), True)])
        df_invalid = self.spark.createDataFrame([(1,), (2,)], schema)
        with self.assertRaises(ValueError):
            summarize_spark_dataframe(df_invalid, 'numbers')

    @classmethod
    def tearDownClass(cls):
        # Stop Spark session
        cls.spark.stop()


if __name__ == '__main__':
    unittest.main()
