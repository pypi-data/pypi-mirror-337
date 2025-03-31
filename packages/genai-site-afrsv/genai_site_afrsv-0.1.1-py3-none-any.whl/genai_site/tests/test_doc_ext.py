import unittest
from unittest.mock import patch, MagicMock
from genai_site.doc_extractor.document_ext import extract_information_from_chunk


class TestExtractInformationFromChunk(unittest.TestCase):
    @patch(
        "genai_site.doc_extractor.document_ext.genai.Client"
    )  # Mock the genai.Client
    def test_extraction(self, mock_genai_client):
        # Mock the behavior of the genai.Client
        mock_client_instance = MagicMock()
        mock_genai_client.return_value = mock_client_instance

        # Mock the response of the generate_content method
        mock_response = MagicMock()
        mock_response.text = "• Key detail 1\n• Key detail 2"
        mock_client_instance.models.generate_content.return_value = mock_response

        # Define test inputs
        google_key = "fake_google_key"
        chunk = "This is a test chunk of text."

        # Call the function
        response = extract_information_from_chunk(chunk, google_key)

        # Assertions
        mock_genai_client.assert_called_once_with(
            api_key=google_key
        )  # Ensure the client is initialized with the correct API key
        mock_client_instance.models.generate_content.assert_called_once_with(
            model="gemini-2.0-flash",
            contents=f"""Analyze the following PDF and extract the most relevant information
            related to the discussed theme. Focus on key details such as landscapes, important
            dates, and any significant contextual elements. Present the extracted information
            in a structured format using bullet points (•) for clarity. Ensure that only the
            most relevant and accurate details are included.

            The provided text chunks are:
            {chunk}""",
        )
        self.assertEqual(
            response, "• Key detail 1\n• Key detail 2"
        )  # Check the returned response


if __name__ == "__main__":
    unittest.main()
