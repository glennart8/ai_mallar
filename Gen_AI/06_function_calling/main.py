"""
Function Calling med Gemini API.
Låt AI anropa dina egna Python-funktioner.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Ladda API-nyckel från .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# Definiera funktioner som AI:n kan anropa
def get_weather(city: str) -> dict:
    """Hämtar väderdata för en stad (simulerad)."""
    # I verkligheten skulle detta anropa ett väder-API
    weather_data = {
        "Stockholm": {"temp": 15, "description": "Molnigt"},
        "Göteborg": {"temp": 17, "description": "Soligt"},
        "Malmö": {"temp": 18, "description": "Delvis molnigt"}
    }
    return weather_data.get(city, {"temp": 0, "description": "Okänd stad"})


def calculate_price(quantity: int, unit_price: float) -> float:
    """Beräknar totalpris."""
    return quantity * unit_price


# Skapa modell med verktyg
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[get_weather, calculate_price]
)

# Starta chat med automatisk funktionsanrop
chat = model.start_chat(enable_automatic_function_calling=True)

# Testa - AI:n väljer automatiskt rätt funktion
response = chat.send_message("Vad är vädret i Stockholm?")
print(response.text)

print("\n---\n")

response = chat.send_message("Vad kostar 5 stycken om styckpriset är 99 kr?")
print(response.text)
