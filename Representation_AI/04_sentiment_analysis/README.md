# Sentiment Analysis

Analysera känsla och ton i text.

## Användning

```python
# Med AI (mer exakt)
result = analyze_sentiment_ai(text)

# Utan API (snabbare, gratis)
result = analyze_sentiment_simple(text)
```

## När använda

- Analysera kundrecensioner
- Övervaka sociala medier
- Kategorisera supportärenden efter ton
- Mäta kundnöjdhet i feedback

## Två metoder

**AI-baserad (Gemini):**
- Mer exakt
- Förstår kontext och nyanser
- Kostar API-anrop

**Regelbaserad:**
- Gratis och snabb
- Enklare logik (ordlistor)
- Missar kontext och ironi

## Output

```python
{
    "sentiment": "positiv",  # positiv/negativ/neutral
    "score": 0.8,            # -1.0 till 1.0
    "explanation": "..."     # (endast AI)
}
```

## Anpassningar

- Utöka ordlistor för din domän
- Lägg till branschspecifika ord
- Justera prompt för andra språk
- Lägg till kategorier (arg, glad, ledsen)
