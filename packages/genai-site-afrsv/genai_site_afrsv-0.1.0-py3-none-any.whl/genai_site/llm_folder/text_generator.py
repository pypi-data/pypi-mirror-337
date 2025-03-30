from google import genai


def run_msg_generator(api_key_, prompt_):
    try:
        client = genai.Client(api_key=str(api_key_))
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"Based on the prompt, generate a detailed image detailing the main features : {prompt_}",
        )
        return response
    except Exception as error:
        print(f"The error {error} is happening.")
