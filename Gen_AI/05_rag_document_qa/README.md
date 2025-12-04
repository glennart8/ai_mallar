# RAG Document QA

Chatta med egna dokument genom Retrieval Augmented Generation.

## Koncept

1. Dela upp dokument i mindre delar
2. Skapa embeddings för varje del
3. Lagra i vector database (ChromaDB)
4. Vid fråga: hämta relevanta delar
5. Skicka delar + fråga till LLM

## Användning

```python
# Indexera dokument
collection.add(
    ids=["1"],
    embeddings=[create_embedding(text)],
    documents=[text]
)

# Ställ fråga
response = ask_question("Din fråga här")
```

## När använda

- Chatbot för intern dokumentation
- Svara på frågor om policydokument
- Sök i kunskapsbaser
- Kundtjänst baserad på FAQ

## Viktiga delar

- `embed_content()` - Skapar vektorer från text
- `collection.add()` - Lagrar dokument i ChromaDB
- `collection.query()` - Söker efter liknande dokument
- Prompt med kontext + fråga
