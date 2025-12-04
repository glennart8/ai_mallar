"""
Textsammanfattning med Gemini API.
Sammanfattar långa texter till kortare versioner.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Ladda API-nyckel från .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Skapa modell
model = genai.GenerativeModel("gemini-1.5-flash")


def summarize(text, max_points=3):
    """Sammanfattar en text till ett antal punkter."""
    prompt = f"""Sammanfatta följande text i {max_points} punkter.
Var koncis och behåll de viktigaste delarna.

Text:
{text}
"""
    response = model.generate_content(prompt)
    return response.text


# Exempeltext
text = """
Artificiell intelligens (AI) är ett brett område inom datavetenskap som
fokuserar på att skapa system som kan utföra uppgifter som normalt kräver
mänsklig intelligens. Detta inkluderar inlärning, problemlösning,
mönsterigenkänning och språkförståelse. Maskininlärning är en undergrupp
av AI där system lär sig från data istället för att vara explicit
programmerade. Djupinlärning är en typ av maskininlärning som använder
neurala nätverk med många lager för att analysera komplexa mönster i data.
"""

result = summarize(text)
print(result)
