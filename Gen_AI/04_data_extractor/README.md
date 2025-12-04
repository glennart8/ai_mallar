# Data Extractor

Extrahera strukturerad data (JSON) från ostrukturerad text.

## Användning

```python
schema = {
    "name": "Personens namn",
    "email": "E-postadress"
}
result = extract_data(text, schema)
```

## När använda

- Extrahera kontaktinfo från emails
- Parsa fakturor och kvitton
- Strukturera data från fritext-rapporter
- Konvertera ostrukturerad data till databas-format

## Viktiga delar

- Definiera ett schema med fältnamn och beskrivningar
- Be modellen returnera ENDAST JSON
- Rensa eventuell markdown-formatering från svaret
- Använd `json.loads()` för att parsa resultatet
