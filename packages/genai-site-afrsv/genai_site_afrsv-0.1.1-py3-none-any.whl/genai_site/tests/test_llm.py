import unittest
from unittest.mock import patch

from genai_site.llm_folder.text_generator import run_msg_generator


class TestLLM(unittest.TestCase):
    @patch(
        "genai_site.llm_folder.text_generator.run_msg_generator"
    )  # Correct target for mocking
    def test_response(self, mock_run_msg_generator):
        # Mock the return value to None
        mock_run_msg_generator.return_value = None
        google_key = "fake_google_key"
        prompt_ = "What is deep learning?"

        # Call the actual function (which is mocked)
        response = run_msg_generator(google_key, prompt_)

        # Assertion to check if response is None
        self.assertIsNone(response)


if __name__ == "__main__":
    unittest.main()
