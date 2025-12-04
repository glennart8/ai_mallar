"""
Enkel AI-agent med Gemini API.
En agent som planerar och utför uppgifter steg-för-steg.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Ladda API-nyckel från .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Skapa modell
model = genai.GenerativeModel("gemini-2.0-flash")


# Tillgängliga verktyg för agenten
def search_info(query: str) -> str:
    """Simulerar en sökning (ersätt med riktig logik)."""
    return f"Sökresultat för '{query}': [Simulerad data]"


def save_note(text: str) -> str:
    """Sparar en anteckning."""
    print(f"[Sparad anteckning]: {text}")
    return "Anteckning sparad."


def send_notification(message: str) -> str:
    """Skickar en notis (simulerad)."""
    print(f"[Notis skickad]: {message}")
    return "Notis skickad."


TOOLS = {
    "search_info": search_info,
    "save_note": save_note,
    "send_notification": send_notification
}


def run_agent(task: str, max_steps: int = 5) -> str:
    """Kör agenten för att utföra en uppgift."""

    context = f"Uppgift: {task}\n\n"

    for step in range(max_steps):
        # Be agenten bestämma nästa steg
        prompt = f"""{context}

Tillgängliga verktyg:
- search_info(query): Sök efter information
- save_note(text): Spara en anteckning
- send_notification(message): Skicka en notis

Vad är nästa steg? Svara med ANTINGEN:
1. TOOL: <verktyg>(argument) - för att använda ett verktyg
2. DONE: <slutsvar> - om uppgiften är färdig

Svar:"""

        response = model.generate_content(prompt)
        response_text = response.text.strip()
        print(f"\nSteg {step + 1}: {response_text}")

        # Kolla om agenten är klar
        if response_text.startswith("DONE:"):
            return response_text.replace("DONE:", "").strip()

        # Kör verktyg om det begärs
        if response_text.startswith("TOOL:"):
            tool_call = response_text.replace("TOOL:", "").strip()
            # Enkel parsing (förenklad)
            for tool_name, function in TOOLS.items():
                if tool_name in tool_call:
                    # Extrahera argument (förenklad)
                    start = tool_call.find("(") + 1
                    end = tool_call.rfind(")")
                    arg = tool_call[start:end].strip("'\"")
                    result = function(arg)
                    context += f"\nSteg {step + 1}: {tool_call}\nResultat: {result}\n"
                    break

    return "Max antal steg uppnådda utan slutförd uppgift."


# Testa agenten
result = run_agent("Sök information om Python och spara en sammanfattning.")
print(f"\nSlutresultat: {result}")
