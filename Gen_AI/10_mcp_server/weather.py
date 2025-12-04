"""
Hämtar väderdata från wttr.in (gratis, ingen API-nyckel).
"""

import httpx


def get_weather(city: str) -> str:
    """Hämtar aktuellt väder för en stad."""
    try:
        # wttr.in returnerar väder som ren text
        # Format: %t = temperatur, %C = beskrivning
        url = f"https://wttr.in/{city}?format=%t,+%C&lang=sv"
        response = httpx.get(url, timeout=10)
        response.raise_for_status()

        return f"{city}: {response.text.strip()}"

    except httpx.HTTPError as e:
        return f"Kunde inte hämta väder: {e}"
