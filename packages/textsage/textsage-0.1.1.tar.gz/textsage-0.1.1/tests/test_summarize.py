import unittest

from textsage.summarize import summarize_text


class TestSummarization(unittest.TestCase):
    def test_summarize_text(self):
        input_text = "Ollama allows running local LLMs efficiently."
        summary = summarize_text(input_text, "mistral")
        self.assertIsInstance(summary, str)
        self.assertGreater(len(summary), 0)


if __name__ == "__main__":
    unittest.main()
