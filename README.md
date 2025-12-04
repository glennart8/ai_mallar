# AI-mallar

Samling av minimala, kopierbara AI-mallar för arbetslivet.

## Installation

```bash
pip install -r requirements.txt
```

Skapa en `.env`-fil i roten med din API-nyckel:

```
GEMINI_API_KEY=din_nyckel_här
```

## Struktur

### Gen_AI - Generativ AI
Mallar som använder Google Gemini för att generera text, analysera bilder, och mer.

| Mall | Beskrivning |
|------|-------------|
| 01_simple_chat | Grundläggande fråga-svar |
| 02_streaming_chat | Realtidsstreaming av svar |
| 03_summarizer | Sammanfatta texter |
| 04_data_extractor | Extrahera strukturerad data från fritext |
| 05_rag_document_qa | Chatta med egna dokument |
| 06_function_calling | Låt AI anropa Python-funktioner |
| 07_image_analyzer | Analysera bilder |
| 08_simple_agent | AI som utför uppgifter steg-för-steg |
| 09_pdf_validator | Validera formulär-PDF:er mot schema |
| 10_mcp_server | MCP-server med verktyg för AI-assistenter |
| 11_mcp_textgame | MCP Resources och State via textäventyr |

### Pred_AI - Prediktiv AI / Machine Learning
Klassiska ML-modeller för prediktion och klassificering.

| Mall | Beskrivning |
|------|-------------|
| 01_linear_regression | Förutsäga numeriska värden |
| 02_classification | Kategorisera data |
| 03_time_series | Prognostisera framtida värden |
| 04_anomaly_detection | Hitta avvikelser i data |

### Representation_AI - Förståelse och Representation
Mallar för att förstå och representera data.

| Mall | Beskrivning |
|------|-------------|
| 01_embeddings_search | Semantisk sökning |
| 02_clustering | Gruppera liknande objekt |
| 03_dimensionality_reduction | Visualisera högdimensionell data |
| 04_sentiment_analysis | Analysera känsla i text |

## Användning

1. Kopiera den mall du vill använda till ditt projekt
2. Installera dependencies från requirements.txt
3. Lägg till din API-nyckel i .env
4. Kör main.py

Varje mall innehåller:
- `main.py` - Minimal, körbar kod
- `README.md` - Förklaring och exempel
