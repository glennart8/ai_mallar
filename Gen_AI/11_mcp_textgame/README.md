# MCP Textäventyr

Lär dig MCP Resources och State genom ett textäventyr!

## Koncept

### Resources vs Tools

```
RESOURCES = Data AI:n kan LÄSA (passivt)
TOOLS     = Aktioner AI:n kan UTFÖRA (aktivt)
```

### I detta exempel

| Typ | Namn | Beskrivning |
|-----|------|-------------|
| Resource | `game://room` | Nuvarande rum och utgångar |
| Resource | `game://inventory` | Spelarens ryggsäck |
| Resource | `game://status` | HP och framsteg |
| Tool | `move(direction)` | Gå i en riktning |
| Tool | `pickup(item)` | Plocka upp föremål |
| Tool | `look()` | Titta dig omkring |
| Tool | `reset()` | Starta om spelet |

### State (Persistent data)

Spelstaten sparas i `game_state.json`:
```json
{
  "current_room": "start",
  "inventory": ["fackla", "rep"],
  "hp": 100,
  "visited_rooms": ["start", "grotta"]
}
```

## Arkitektur

```
┌─────────────────────────────────────────────────────────────┐
│                      AI-KLIENT                              │
│  "Gå norrut och plocka upp facklan"                         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                    MCP-protokoll
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                     MCP-SERVER                              │
│                                                             │
│  RESOURCES (läsa)              TOOLS (agera)                │
│  ┌───────────────────┐         ┌───────────────────┐        │
│  │ game://room       │         │ move(direction)   │        │
│  │ game://inventory  │         │ pickup(item)      │        │
│  │ game://status     │         │ look()            │        │
│  └─────────┬─────────┘         └─────────┬─────────┘        │
│            │                             │                  │
│            └──────────┬──────────────────┘                  │
│                       ▼                                     │
│              ┌─────────────────┐                            │
│              │ game_state.json │  ← Persistent state        │
│              └─────────────────┘                            │
└─────────────────────────────────────────────────────────────┘
```

## Spelkarta

```
                    ┌─────────────┐
                    │   SKATT     │
                    │ (kräver     │
                    │  fackla)    │
                    └──────┬──────┘
                           │ upp/ner
                    ┌──────▼──────┐
                    │   GROTTA    │
                    │  [fackla]   │
                    └──────┬──────┘
                           │ norr/söder
┌─────────────┐     ┌──────▼──────┐
│     Ö       │◄────│   START     │
│ (kräver rep)│över │  [pinne]    │
│[magisk_sten]│     └──────┬──────┘
└─────────────┘            │ öster/väster
                    ┌──────▼──────┐
                    │    FLOD     │
                    │   [rep]     │
                    └─────────────┘
```

## Användning

### Testa med Claude Desktop

Lägg till i `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "textgame": {
      "command": "python",
      "args": ["C:/path/to/server.py"]
    }
  }
}
```

### Exempel-dialog

```
Du: Var är jag?
AI: [läser game://room]
    📍 Skogsgläntan
    Du står i en solig skogsglänta. Fåglar kvittrar.
    Du ser: pinne
    Utgångar: norr, öster

Du: Gå norrut
AI: [anropar move("norr")]
    📍 Mörk grotta
    En fuktig grotta. Du hör droppande vatten.
    Du ser: fackla
    Utgångar: söder, ner

Du: Plocka upp facklan
AI: [anropar pickup("fackla")]
    Du plockar upp 'fackla'!

Du: Gå ner
AI: [anropar move("ner")]
    📍 Skattkammaren
    En glittrande kammare full av guld!
    Du ser: guldmynt, krona
```

## Filer

| Fil | Beskrivning |
|-----|-------------|
| `server.py` | MCP-server med Resources och Tools |
| `game.py` | Spellogik och state-hantering |
| `game_state.json` | Sparad speldata (skapas automatiskt) |
