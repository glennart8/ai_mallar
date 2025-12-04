# Summarizer

Sammanfatta långa texter till kortare versioner.

## Användning

```python
def summarize(text, max_points=3):
    prompt = f"Sammanfatta följande text i {max_points} punkter: {text}"
    response = model.generate_content(prompt)
    return response.text
```

## När använda

- Sammanfatta rapporter och dokument
- Skapa översikter av mötesanteckningar
- Komprimera långa artiklar
- Extrahera huvudpunkter från email-trådar

## Anpassningar

- Ändra `max_points` för längre/kortare sammanfattningar
- Lägg till instruktioner för ton eller format
- Specificera vilken typ av information som ska prioriteras
