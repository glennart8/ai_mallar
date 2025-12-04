"""
Sentiment Analysis - Analysera känsla/ton i text.
Två metoder: Gemini API och regelbaserad.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Ladda API-nyckel från .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def analyze_sentiment_ai(text: str) -> dict:
    """Analyserar sentiment med Gemini API."""
    prompt = f"""Analysera sentimentet i följande text.
Returnera ENDAST en rad med format: SENTIMENT|SCORE|FÖRKLARING
- SENTIMENT: positiv, negativ, eller neutral
- SCORE: -1.0 till 1.0 (negativ till positiv)
- FÖRKLARING: kort förklaring (max 10 ord)

Text: {text}
"""
    response = model.generate_content(prompt)
    parts = response.text.strip().split("|")

    return {
        "sentiment": parts[0].strip().lower(),
        "score": float(parts[1].strip()),
        "explanation": parts[2].strip() if len(parts) > 2 else ""
    }


def analyze_sentiment_simple(text: str) -> dict:
    """Enkel regelbaserad sentimentanalys (utan API)."""
    positive_words = ["bra", "fantastisk", "nöjd", "rekommenderar", "utmärkt", "perfekt"]
    negative_words = ["dålig", "hemskt", "besviken", "problem", "trasig", "värdelöst"]

    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)

    if pos_count > neg_count:
        return {"sentiment": "positiv", "score": min(pos_count * 0.3, 1.0)}
    elif neg_count > pos_count:
        return {"sentiment": "negativ", "score": max(-neg_count * 0.3, -1.0)}
    else:
        return {"sentiment": "neutral", "score": 0.0}


# Testa med exempel
texts = [
    "Produkten är fantastisk! Helt perfekt, rekommenderar verkligen.",
    "Dålig kvalitet och trasig redan efter en vecka. Hemskt besviken.",
    "Produkten kom fram i tid. Den fungerar som förväntat."
]

print("Sentiment Analysis med Gemini API:\n")
for text in texts:
    result = analyze_sentiment_ai(text)
    print(f"Text: {text[:50]}...")
    print(f"  Sentiment: {result['sentiment']} ({result['score']:+.2f})")
    print(f"  Förklaring: {result['explanation']}\n")
