# Function Calling

Låt AI anropa dina egna Python-funktioner automatiskt.

## Koncept

1. Definiera Python-funktioner med typehints och docstrings
2. Ge funktionerna till modellen som verktyg
3. AI:n väljer automatiskt vilken funktion som passar
4. Resultatet används i svaret

## Användning

```python
def my_function(param: str) -> dict:
    """Beskrivning av vad funktionen gör."""
    return {"result": "data"}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[my_function]
)

chat = model.start_chat(enable_automatic_function_calling=True)
response = chat.send_message("Använd funktionen...")
```

## När använda

- Integrera AI med befintliga system (databaser, API:er)
- Låt AI utföra åtgärder (skicka email, skapa uppgifter)
- Koppla AI till realtidsdata (väder, aktiekurser)
- Bygg chatbots som kan göra saker

## Viktiga delar

- Funktioner måste ha typehints och docstrings
- `tools=[function1, function2]` ger modellen tillgång
- `enable_automatic_function_calling=True` anropar automatiskt
