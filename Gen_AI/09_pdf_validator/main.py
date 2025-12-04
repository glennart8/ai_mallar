"""
PDF-validering med Gemini API.
Validerar formulär-PDF:er mot ett definierat schema.
"""

import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from pypdf import PdfReader
from schema import SCHEMA

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Skapa modell
model = genai.GenerativeModel("gemini-2.0-flash")

""" UTVECKLING
1. Lägg in funktioner för att hämta pdf från mail, sedan läsa, validera och autogenerera mailsvar
2. Batch-rapport: Validera alla PDF:er och generera en sammanfattande Excel/CSV med status
3. Webb-gränssnitt: Enkel Streamlit-app där användare kan ladda upp PDF och se resultat direkt
4. Webhook/notifikation: Skicka Slack/Teams-meddelande när validering är klar
5. Multi-schema: Stöd för olika formulärtyper (bidrag, faktura, avtal) med dynamiskt val av schema
"""

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extraherar all text från en PDF-fil."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def validate_pdf(pdf_path: str, schema: dict = SCHEMA) -> dict:
    """
    Validerar en PDF mot ett schema.

    Args:
        pdf_path: Sökväg till PDF-filen
        schema: Dict med förväntade fält och valideringsregler

    Returns:
        Dict med valideringsresultat (valid, errors, extracted_data)
    """
    # Extrahera text från PDF
    pdf_text = extract_text_from_pdf(pdf_path)

    # Skapa prompt för Gemini
    schema_json = json.dumps(schema, ensure_ascii=False, indent=2)

    # Skapa lista över obligatoriska och valfria fält
    required_fields = [f for f, r in schema.items() if r.get("required", False)]
    optional_fields = [f for f, r in schema.items() if not r.get("required", False)]

    prompt = f"""Validera formuläret mot schemat.

OBLIGATORISKA FÄLT (skapa FEL om de saknas):
{required_fields}

VALFRIA FÄLT (INGET FEL om de saknas):
{optional_fields}

SCHEMA MED DETALJER:
{schema_json}

FORMULÄRTEXT:
{pdf_text}

REGLER:
1. Saknas ett OBLIGATORISKT fält → lägg till i errors
2. Saknas ett VALFRITT fält → LÄGG INTE till i errors
3. Om min_length finns och texten är för kort → lägg till i errors
4. valid = true endast om errors är tom

RETURNERA ENDAST JSON:
{{
    "valid": true/false,
    "errors": [{{"field": "fältnamn", "error": "beskrivning"}}],
    "extracted_data": {{"fält": "värde eller null"}}
}}
"""

    response = model.generate_content(prompt)

    # Rensa eventuell markdown-formatering
    json_text = response.text.strip()
    if json_text.startswith("```"):
        json_text = json_text.split("\n", 1)[1]
        json_text = json_text.rsplit("```", 1)[0]

    result = json.loads(json_text)

    # Extra Python-validering för logiska kontroller
    result = _validate_business_rules(result)

    return result


def _validate_business_rules(result: dict) -> dict:
    """Validerar affärslogik som AI inte kan kontrollera pålitligt."""
    extracted = result.get("extracted_data", {})
    errors = result.get("errors", [])

    # Kontrollera att sökt belopp inte överstiger budget
    try:
        budget_num = int(str(extracted.get("budget")).replace(" ", ""))
        sokt_num = int(str(extracted.get("sokt_belopp")).replace(" ", ""))

        if sokt_num > budget_num:
            errors.append({
                "field": "sokt_belopp",
                "error": f"Sökt belopp ({sokt_num} kr) överstiger total budget ({budget_num} kr)"
            })
    except (ValueError, TypeError):
        pass  # Saknas eller inte numeriska värden

    result["errors"] = errors
    result["valid"] = len(errors) == 0

    return result


def print_validation_result(result: dict):
    """Skriver ut valideringsresultatet på ett läsbart sätt."""
    print("VALIDERINGSRESULTAT")

    if result["valid"]:
        print("\nSTATUS: GODKÄND")
    else:
        print("\nSTATUS: UNDERKÄND")

    if result["errors"]:
        print("\nFEL:")
        for error in result["errors"]:
            print(f"  - {error['field']}: {error['error']}")

    print("\nEXTRAHERAD DATA:")
    for field, value in result["extracted_data"].items():
        display_value = value if value else "(Saknas)"
        print(f"{field}: {display_value}")

    print("============================================")


# Testa validering
if __name__ == "__main__":
    import time
    from pathlib import Path
    
    result = validate_pdf("data/invalid_application.pdf")
    print_validation_result(result)


    # # Validera alla PDF:er i data-mappen
    # pdf_files = list(Path("data").glob("*.pdf"))

    # for i, pdf_file in enumerate(pdf_files):
    #     print(f"\n {pdf_file.name}")
    #     result = validate_pdf(str(pdf_file))
    #     print_validation_result(result)

    #     # Paus mellan anrop för att undvika rate limit
    #     if i < len(pdf_files) - 1:
    #         time.sleep(2)
