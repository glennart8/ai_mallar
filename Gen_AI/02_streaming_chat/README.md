# Streaming Chat

Realtidsstreaming av svar från Gemini API.

## Användning

```python
response = model.generate_content(question, stream=True)
for chunk in response:
    print(chunk.text, end="", flush=True)
```

## När använda

- Längre svar där användaren vill se progressen
- Chat-gränssnitt som visar text medan den skrivs
- Bättre användarupplevelse för interaktiva applikationer

## Viktiga delar

- `stream=True` - Aktiverar streaming
- `flush=True` - Tvingar utskrift direkt utan buffring
- Iterera över `response` för att få varje chunk
