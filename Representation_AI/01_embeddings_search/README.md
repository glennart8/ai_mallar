# Embeddings Search

Semantisk sökning - hitta liknande texter baserat på betydelse.

## Koncept

1. Konvertera text till vektor (embedding)
2. Vektorer som ligger nära = liknande betydelse
3. Sök med cosine similarity

## Användning

```python
# Skapa embedding
vector = create_embedding("Min text")

# Jämför två texter
similarity = cosine_similarity(vector1, vector2)
# Nära 1.0 = mycket lika, nära 0 = olika
```

## När använda

- Semantisk dokumentsökning
- Hitta liknande artiklar/produkter
- Duplicate detection
- FAQ-matchning
- Rekommendationssystem

## Skillnad mot nyckelordssökning

Nyckelord: "bil" hittar INTE "fordon"
Semantisk: "bil" HITTAR "fordon" (liknande betydelse)

## Viktiga delar

- `embed_content()` - Geminis embedding-API
- `cosine_similarity()` - Mäter vinkel mellan vektorer
- Högre värde = mer lika (max 1.0)

## Optimering

- För stora datamängder: använd vector database (ChromaDB, Pinecone)
- Cacha embeddings (dyrt att beräkna om)
- Batch-skapa embeddings för effektivitet
