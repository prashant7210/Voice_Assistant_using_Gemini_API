import google.generativeai as genai
from config import apikey

genai.configure(api_key=apikey)
myfile = genai.upload_file("imgage.jpg")

model = genai.GenerativeModel("gemini-1.5-flash")
result = model.generate_content(
    [myfile, "\n\n", "Can you tell me about the instruments in this photo?"]
)


print(result.text)