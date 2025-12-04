"""
Streaming chat med Gemini API.
Visar svaret i realtid medan det genereras.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Ladda API-nyckel från .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Skapa modell
model = genai.GenerativeModel("gemini-1.5-flash")

# Skicka fråga med streaming
question = "Förklara hur en dator fungerar."
response = model.generate_content(question, stream=True)

# Skriv ut varje chunk direkt
for chunk in response:
    print(chunk.text, end="", flush=True)

print()  # Ny rad efter svaret
