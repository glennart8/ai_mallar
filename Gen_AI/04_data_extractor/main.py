"""
Data extraktion med Gemini API.
Extraherar strukturerad data (JSON) från ostrukturerad text.
"""

import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Ladda API-nyckel från .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Skapa modell
model = genai.GenerativeModel("gemini-1.5-flash")


def extract_data(text, schema):
    """Extraherar data enligt ett schema från fritext."""
    prompt = f"""Extrahera följande information från texten och returnera som JSON.
Returnera ENDAST JSON, ingen annan text.

Schema (fält att extrahera):
{json.dumps(schema, ensure_ascii=False, indent=2)} 

Text:
{text}
"""
    response = model.generate_content(prompt)

    # Rensa eventuell markdown-formatering
    json_text = response.text.strip()
    if json_text.startswith("```"):
        json_text = json_text.split("\n", 1)[1]
        json_text = json_text.rsplit("```", 1)[0]

    return json.loads(json_text)


# Exempel: extrahera kontaktinfo från ett email
email_text = """
Hej,

Jag heter Anna Andersson och är intresserad av era tjänster.
Ni kan nå mig på anna.andersson@foretag.se eller 070-123 45 67.
Jag jobbar på TechAB som projektledare.

Med vänlig hälsning,
Anna
"""

schema = {
    "name": "Personens fullständiga namn",
    "email": "E-postadress",
    "phone": "Telefonnummer",
    "company": "Företagsnamn",
    "title": "Jobbtitel"
}

result = extract_data(email_text, schema)
print(json.dumps(result, ensure_ascii=False, indent=2))
