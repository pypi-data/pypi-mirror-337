import unittest

from textsage.llm_utils import summarize_text, analyze_sentiment, extract_key_phrases


class TestLLMUtils(unittest.TestCase):
    def test_summarize_text(self):
        input_text = "Ollama allows running local LLMs efficiently."
        summary = summarize_text(input_text, "mistral")
        self.assertIsInstance(summary, str)
        self.assertGreater(len(summary), 0)

    def test_analyze_sentiment(self):
        input_text = "I love using Ollama for local LLMs!"
        sentiment = analyze_sentiment(input_text, "mistral")
        self.assertIsInstance(sentiment, dict)
        self.assertIn("positive", sentiment)
        self.assertIn("negative", sentiment)
        self.assertIn("neutral", sentiment)

    def test_extract_key_phrases(self):
        input_text = "Ollama allows running local LLMs efficiently."
        key_phrases = extract_key_phrases(input_text, "mistral")
        self.assertIsInstance(key_phrases, list)
        self.assertGreater(len(key_phrases), 0)


if __name__ == "__main__":
    unittest.main()
