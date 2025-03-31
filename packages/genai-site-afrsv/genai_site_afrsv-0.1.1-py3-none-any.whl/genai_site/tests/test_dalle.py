import unittest
from unittest.mock import patch

from genai_site.img_generator.image_generator import run_img_generator


class TestLLM(unittest.TestCase):
    @patch("genai_site.img_generator.image_generator.run_img_generator")
    def test_response(self, mock_run_img_generator):
        # Mock the return value of run_img_generator
        mock_run_img_generator.return_value = None
        google_key = "fake_google_key"
        prompt_ = "What is deep learning?"

        # Call the function
        response = run_img_generator(google_key, prompt_)

        # Assertions
        self.assertIsNone(response)


if __name__ == "__main__":
    unittest.main()
