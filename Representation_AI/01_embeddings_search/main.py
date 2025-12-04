"""
Embeddings och Semantisk Sökning med Gemini API.
Hitta liknande texter baserat på betydelse, inte nyckelord.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
import numpy as np

# Ladda API-nyckel från .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def create_embedding(text: str) -> list:
    """Skapar en embedding-vektor för en text."""
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text
    )
    return result["embedding"]


def cosine_similarity(vec1: list, vec2: list) -> float:
    """Beräknar cosine similarity mellan två vektorer."""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


# Exempeldokument att söka i
documents = [
    "Python är ett populärt programmeringsspråk för dataanalys",
    "Maskininlärning används för att bygga prediktiva modeller",
    "Stockholm är Sveriges huvudstad och största stad",
    "Kaffe är en populär dryck på morgonen",
    "Deep learning är en del av artificiell intelligens"
]

# Skapa embeddings för alla dokument
print("Skapar embeddings för dokument...")
doc_embeddings = [create_embedding(doc) for doc in documents]


def search(query: str, top_n: int = 3) -> list:
    """Söker efter de mest relevanta dokumententen."""
    query_embedding = create_embedding(query)

    # Beräkna likhet med alla dokument
    similarities = []
    for i, doc_emb in enumerate(doc_embeddings):
        similarity = cosine_similarity(query_embedding, doc_emb)
        similarities.append((similarity, documents[i]))

    # Sortera och returnera topp N
    similarities.sort(reverse=True)
    return similarities[:top_n]


# Testa sökning
queries = [
    "Hur gör man AI?",
    "Vad är bra att dricka?",
    "programmering och kod"
]

for query in queries:
    print(f"\nSökning: '{query}'")
    results = search(query, top_n=2)
    for similarity, doc in results:
        print(f"  [{similarity:.3f}] {doc}")
