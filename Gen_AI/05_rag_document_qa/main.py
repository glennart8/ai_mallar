"""
RAG (Retrieval Augmented Generation) med Gemini API.
Chatta med egna dokument genom att hämta relevant kontext.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
import chromadb

# Ladda API-nyckel från .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Skapa modell och embedding-funktion
model = genai.GenerativeModel("gemini-2.5-flash")


def create_embedding(text):
    """Skapar en embedding-vektor för en text."""
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text
    )
    return result["embedding"]


# Skapa vector store
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="documents")

# Exempeldokument att indexera
documents = [
    "Företaget grundades 2010 och har huvudkontor i Stockholm.",
    "Vi erbjuder tjänster inom mjukvaruutveckling och IT-konsulting.",
    "Öppettider är måndag till fredag 08:00-17:00.",
    "Kontakta oss på info@foretag.se eller 08-123 45 67."
]

# Indexera dokumenten
for i, doc in enumerate(documents):
    collection.add(
        ids=[str(i)],
        embeddings=[create_embedding(doc)],
        documents=[doc]
    )


def ask_question(question, num_results=2):
    """Ställer en fråga och använder relevanta dokument som kontext."""
    # Hämta relevanta dokument
    results = collection.query(
        query_embeddings=[create_embedding(question)],
        n_results=num_results
    )
    context = "\n".join(results["documents"][0])

    # Skapa prompt med kontext
    prompt = f"""Baserat på följande information, svara på frågan.
Om informationen inte räcker, säg det.

Information:
{context}

Fråga: {question}
"""
    response = model.generate_content(prompt)
    return response.text


# Testa
print(ask_question("Vilka tjänster erbjuder företaget?"))
print("\n---\n")
print(ask_question("Hur kontaktar jag företaget?"))
