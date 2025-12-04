"""
Enkel chat med Gemini API.
Skickar en fråga och får ett svar.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Ladda API-nyckel från .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Skapa modell
model = genai.GenerativeModel("gemini-1.5-flash")

# Skicka fråga och skriv ut svar
question = "Vad är artificiell intelligens?"
response = model.generate_content(question)
print(response.text)
