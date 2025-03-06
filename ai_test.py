import google.generativeai as genai
from config import apikey

def ai(prompt):
    genai.configure(api_key=apikey)
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 256,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    )

    chat_session = model.start_chat()

    response = chat_session.send_message(prompt)
    new_res = response.text
    new_res = new_res.replace("*", "")
    new_res = new_res.replace("#", "")

    return new_res


print(ai("Tell me about yourself"))