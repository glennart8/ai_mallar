# Simple Chat

Grundläggande fråga-svar med Gemini API.

## Användning

```python
question = "Din fråga här"
response = model.generate_content(question)
print(response.text)
```

## När använda

- Enkla frågor som inte kräver kontext
- Snabba svar utan konversationshistorik
- Prototyping och testning

## Viktiga delar

- `genai.configure()` - Konfigurerar API-nyckeln
- `GenerativeModel()` - Skapar en modellinstans
- `generate_content()` - Skickar prompt och får svar
