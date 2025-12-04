# MCP Server

Enkel MCP-server (Model Context Protocol) som exponerar verktyg till AI-assistenter.

## Vad är MCP?

MCP är Anthropics öppna standard för att koppla AI-assistenter till externa verktyg och datakällor. En MCP-server kan exponera:

- **Tools** - Funktioner som AI:n kan anropa
- **Resources** - Data som AI:n kan läsa
- **Prompts** - Fördefinierade promptmallar

## Arkitektur

```
┌─────────────────────────────────────────────────────────────┐
│                        AI-KLIENT                            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │  Användare  │───▶│   Gemini    │───▶│ MCP-klient  │     │
│  └─────────────┘    └─────────────┘    └──────┬──────┘     │
└───────────────────────────────────────────────┼─────────────┘
                                                │
                              MCP-protokoll (stdio)
                                                │
┌───────────────────────────────────────────────▼─────────────┐
│                       MCP-SERVER                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │    add()    │  │ multiply()  │  │get_weather()│   ...   │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## Flöde: Användare → AI → Tool → Svar

```
1. Användare: "Vad är 15 * 8?"
        │
        ▼
2. Gemini analyserar frågan och ser tillgängliga verktyg
        │
        ▼
3. Gemini bestämmer: "Jag behöver använda multiply()"
        │
        ▼
4. AI-klienten anropar MCP-servern: multiply(a=15, b=8)
        │
        ▼
5. MCP-servern kör funktionen och returnerar: 120
        │
        ▼
6. Resultatet skickas tillbaka till Gemini
        │
        ▼
7. Gemini formulerar svar: "15 gånger 8 är 120."
```

## Installation

```bash
pip install -r requirements.txt
```

## Användning

### Alternativ 1: Enkel test-klient

```bash
python client.py
```

Startar servern, listar verktyg och testar alla funktioner automatiskt.

### Alternativ 2: AI-klient med Gemini

```bash
python ai_client.py
```

Chatta med Gemini som automatiskt använder MCP-verktygen vid behov.

### Alternativ 3: Claude Desktop

Lägg till i `claude_desktop_config.json`:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "demo": {
      "command": "python",
      "args": ["C:/full/path/to/server.py"]
    }
  }
}
```

## Filer

| Fil | Beskrivning |
|-----|-------------|
| `server.py` | MCP-servern som exponerar verktyg |
| `client.py` | Enkel test-klient utan AI |
| `ai_client.py` | AI-klient som kopplar Gemini till verktygen |

## Tillgängliga verktyg

| Verktyg | Beskrivning |
|---------|-------------|
| `add(a, b)` | Adderar två tal |
| `multiply(a, b)` | Multiplicerar två tal |
| `get_weather(city)` | Hämtar väder (mock) |
| `reverse_string(text)` | Vänder på en sträng |

## Skapa egna verktyg

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Min Server")

@mcp.tool()
def my_function(param: str) -> str:
    """Beskrivning av vad funktionen gör."""
    return f"Resultat: {param}"
```

## Länkar

- [MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
