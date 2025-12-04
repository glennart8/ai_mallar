# Varför MCP?

## Problemet utan MCP

Utan en standard måste varje AI-integration byggas från grunden:

```
┌─────────────┐     Egen kod      ┌─────────────┐
│   Claude    │◄─────────────────►│  Din app    │
└─────────────┘                   └─────────────┘
┌─────────────┐     Annan kod     ┌─────────────┐
│   Gemini    │◄─────────────────►│  Din app    │
└─────────────┘                   └─────────────┘
┌─────────────┐     Tredje kod    ┌─────────────┐
│   GPT-4     │◄─────────────────►│  Din app    │
└─────────────┘                   └─────────────┘
```

Varje AI kräver sin egen implementation. Byter du AI måste du skriva om integrationen.

## Lösningen med MCP

MCP (Model Context Protocol) är en öppen standard som definierar hur AI-assistenter kommunicerar med externa system:

```
┌─────────────┐                   ┌─────────────┐
│   Claude    │◄──┐               │             │
└─────────────┘   │               │             │
┌─────────────┐   │     MCP       │  Din app    │
│   Gemini    │◄──┼──────────────►│  (server)   │
└─────────────┘   │               │             │
┌─────────────┐   │               │             │
│   GPT-4     │◄──┘               └─────────────┘
└─────────────┘
```

**En integration fungerar med alla AI-modeller.**

## MCPs tre byggstenar

### 1. Tools (Verktyg)
Funktioner som AI:n kan **anropa** för att utföra aktioner.

```python
@mcp.tool()
def move(direction: str) -> str:
    """Flyttar spelaren i en riktning."""
    return game.move(direction)
```

**Kännetecken:**
- Ändrar tillstånd (state)
- Har sidoeffekter
- AI:n bestämmer när de anropas

### 2. Resources (Resurser)
Data som AI:n kan **läsa** för att få information.

```python
@mcp.resource("game://room")
def get_current_room() -> str:
    """Visar nuvarande rum."""
    return game.get_room_info()
```

**Kännetecken:**
- Endast läsning
- Inga sidoeffekter
- Ger AI:n kontext

### 3. Prompts (Promptmallar)
Fördefinierade instruktioner som AI:n kan använda.

```python
@mcp.prompt()
def analyze_code(language: str) -> str:
    """Analysera kod på ett visst språk."""
    return f"Analysera följande {language}-kod..."
```

## Varför detta spelar roll

### Separation of Concerns
MCP tvingar fram en tydlig uppdelning:
- **Server** = Exponerar funktionalitet
- **Klient** = Konsumerar funktionalitet
- **AI** = Bestämmer vad som ska göras

### Återanvändbarhet
En MCP-server kan användas av:
- Claude Desktop
- VS Code med Copilot
- Egen AI-klient
- Vilken MCP-kompatibel applikation som helst

### Säkerhet
AI:n kan bara göra det servern tillåter. Du kontrollerar exakt vilka verktyg som exponeras.

## I detta textäventyr

```
┌────────────────┐
│  ai_client.py  │  ← Gemini bestämmer vilka tools att använda
└───────┬────────┘
        │ MCP (stdio)
        ▼
┌────────────────┐
│   server.py    │  ← Exponerar tools och resources
└───────┬────────┘
        │ Python-anrop
        ▼
┌────────────────┐
│    game.py     │  ← Spellogik och state
└────────────────┘
```

**Utan MCP** hade Gemini-integrationen varit hårdkodad mot spellogiken.

**Med MCP** kan vi byta ut Gemini mot Claude utan att ändra en rad i server.py eller game.py.

## Sammanfattning

| Utan MCP | Med MCP |
|----------|---------|
| Egen kod per AI | En standard för alla |
| Tight coupling | Loose coupling |
| Svårt att byta AI | Enkelt att byta AI |
| Säkerhet är ditt problem | Kontrollerad exponering |

MCP är för AI-integrationer vad REST är för web-API:er - en gemensam standard som gör ekosystemet interoperabelt.
