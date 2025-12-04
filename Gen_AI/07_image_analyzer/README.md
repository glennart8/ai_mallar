# Image Analyzer

Analysera bilder med Gemini Vision.

## Användning

```python
# Från lokal fil
response = analyze_image("dokument.jpg", "Vad står på detta dokument?")

# Från URL
response = analyze_image_url("https://...", "Beskriv bilden")
```

## När använda

- Extrahera text från kvitton och fakturor
- Analysera diagram och grafer
- Kategorisera bilder automatiskt
- OCR för handskriven text
- Beskriva bildinnehåll

## Exempel på frågor

- "Extrahera alla siffror från detta kvitto"
- "Vad visar detta diagram?"
- "Finns det någon text i bilden?"
- "Beskriv vad som händer i bilden"
- "Vilken produkt är detta?"

## Viktiga delar

- `genai.upload_file()` - Laddar upp bild till API
- Skicka [image, text] till `generate_content()`
- Stödjer JPG, PNG, GIF, WebP
