"""
Bildanalys med Gemini API.
Analysera bilder och extrahera information.
"""

import os

# Dölj grpc-varningar (ALTS)
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

from dotenv import load_dotenv
import google.generativeai as genai
from pathlib import Path

# Ladda API-nyckel från .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Skapa modell (måste vara en vision-modell)
model = genai.GenerativeModel("gemini-2.0-flash")


def analyze_image(image_path: str, question: str) -> str:
    """Analyserar en bild och svarar på en fråga om den."""
    # Ladda bild
    image = genai.upload_file(image_path)

    # Skicka bild + fråga
    response = model.generate_content([image, question])
    return response.text


def analyze_image_url(image_url: str, question: str) -> str:
    """Analyserar en bild från URL."""
    import urllib.request

    # Ladda ner bilden temporärt
    temp_path = "temp_image.jpg"
    urllib.request.urlretrieve(image_url, temp_path)

    result = analyze_image(temp_path, question)

    # Ta bort temporär fil
    os.remove(temp_path)
    return result

try:
    response = analyze_image("data/bild.jpg", "Vilken typ av restaurang föreställer bilden?")
    print(response)
except Exception as e:
    print(f"Ett fel uppstod: {e}")

