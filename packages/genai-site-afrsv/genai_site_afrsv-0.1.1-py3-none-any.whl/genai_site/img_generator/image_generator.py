from google import genai
from google.genai import types


def run_img_generator(api_key_, prompt_):
    try:
        client = genai.Client(api_key=str(api_key_))
        contents = f"According to the prompt, generate a detailed image : {prompt_}"
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
            contents=contents,
            config=types.GenerateContentConfig(response_modalities=["Text", "Image"]),
        )
        return response
    except Exception as error:
        print(f"The error {error} is happening.")
        return None
