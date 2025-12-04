# PDF Validator

Validera formulär-PDF:er mot ett definierat schema med Gemini API.

## Användning

```bash
# 1. Skapa test-PDF:er
python create_test_pdf.py

# 2. Validera alla PDF:er i data-mappen
python main.py
```

## Schema

Schemat finns i `schema.py` och definierar vilka fält som förväntas:

```python
SCHEMA = {
    "namn": {"required": True, "description": "För- och efternamn"},
    "email": {"required": True, "format": "Giltig e-postadress"},
    "beskrivning": {"required": True, "min_length": 100},
}
```

**Egenskaper:**
- `required` - Obligatoriskt fält (true/false)
- `format` - Förväntat format (e-post, organisationsnummer, etc.)
- `min_length` - Minsta antal tecken
- `description` - Beskrivning av fältet

## Output

```python
{
    "valid": False,
    "errors": [
        {"field": "email", "error": "Felaktigt format"}
    ],
    "extracted_data": {
        "namn": "Anna Svensson",
        "email": "anna@"
    }
}
```

## Anpassa för egna formulär

1. Ändra `SCHEMA` i `schema.py` till dina fält
2. Uppdatera `create_test_pdf.py` för att generera matchande testformulär
3. Kör validering

## Begränsningar

- Fungerar bäst med textbaserade PDF:er (inte skannade bilder)
- AI:n tolkar fältnamn - testa med dina specifika formulär
