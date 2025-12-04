# Utvecklingsidéer för textäventyret

Sorterade från enklast till mest avancerat.

## Nivå 1: Enkla tillägg (1-2 funktioner)

### 1. HP-system med skada
Rum som skadar spelaren när man går in.
```python
# world.py
"fängelse": {
    "damage": 10,  # Tar 10 HP
    ...
}

# game.py - i move()
if new_room.get("damage"):
    state["hp"] -= new_room["damage"]
    if state["hp"] <= 0:
        return "Du dog! Game over."
```

### 2. Healing-föremål
Föremål som återställer HP när de används.
```python
# server.py
@mcp.tool()
def use(item: str) -> str:
    """Använd ett föremål."""
    return game.use_item(item)

# game.py
HEALING_ITEMS = {"äpple": 20, "hälsodryck": 50}

def use_item(item: str) -> str:
    if item in HEALING_ITEMS:
        state["hp"] = min(100, state["hp"] + HEALING_ITEMS[item])
        state["inventory"].remove(item)
        return f"Du använder {item} och återfår HP!"
```

### 3. Förbrukningsbara nycklar
Nycklar som försvinner när de används.
```python
# world.py
"bibliotek": {
    "consumes": "rostig_nyckel",  # Förbrukas vid inträde
    ...
}

# game.py - i move()
if new_room.get("consumes"):
    key = new_room["consumes"]
    state["inventory"].remove(key)
```

### 4. Hint-resource
En resource som ger spelaren ledtrådar.
```python
# world.py - lägg till i varje rum
"grotta": {
    "hint": "Det luktar rök längre ner...",
    ...
}

# server.py
@mcp.resource("game://hint")
def get_hint() -> str:
    """Ger en ledtråd för nuvarande rum."""
    return game.get_hint()
```

### 5. Undersök föremål
Tool för att få mer info om saker i rummet.
```python
# world.py
"items": {
    "fackla": {"description": "En tjärdränkt fackla. Kan lysa upp mörka platser."},
    "rep": {"description": "Ett starkt rep. Användbart för klättring."}
}

# server.py
@mcp.tool()
def examine(item: str) -> str:
    """Undersök ett föremål närmare."""
    return game.examine_item(item)
```

---

## Nivå 2: Mellannivå (ny mekanik)

### 6. Fiender och strid
Monster som blockerar vägen och kräver vapen.
```python
# world.py
"fängelse": {
    "enemy": {
        "name": "Skuggvarelse",
        "requires_weapon": "silverdolk",
        "damage": 20
    }
}

# server.py
@mcp.tool()
def attack(weapon: str) -> str:
    """Attackera en fiende med ett vapen."""
    return game.attack_enemy(weapon)

# game.py
def attack_enemy(weapon: str) -> str:
    room = get_current_room()
    enemy = room.get("enemy")
    if not enemy:
        return "Det finns ingen att attackera här."
    if weapon != enemy["requires_weapon"]:
        state["hp"] -= enemy["damage"]
        return f"{enemy['name']} attackerar dig! Du tar {enemy['damage']} skada."
    room["enemy"] = None  # Fienden är besegrad
    return f"Du besegrar {enemy['name']}!"
```

### 7. NPCs och dialog
Karaktärer man kan prata med.
```python
# world.py
"hall": {
    "npc": {
        "name": "Gammal vakt",
        "dialog": [
            "Välkommen, främling.",
            "Akta dig för det som lurar i fängelsehålan.",
            "Jag har sagt allt jag vet."
        ]
    }
}

# server.py
@mcp.tool()
def talk() -> str:
    """Prata med en karaktär i rummet."""
    return game.talk_to_npc()
```

### 8. Handel
Köp och sälj föremål.
```python
# world.py
"marknad": {
    "shop": {
        "hälsodryck": {"price": 10, "stock": 3},
        "silverdolk": {"price": 50, "stock": 1}
    }
}

# game.py - lägg till i state
"gold": 0

# server.py
@mcp.tool()
def buy(item: str) -> str:
    """Köp ett föremål."""
    return game.buy_item(item)

@mcp.tool()
def sell(item: str) -> str:
    """Sälj ett föremål."""
    return game.sell_item(item)
```

### 9. Tidsbegränsning
Antal drag innan något händer.
```python
# game.py - lägg till i state
"turns": 0,
"max_turns": 100

# I varje tool-anrop
state["turns"] += 1
if state["turns"] >= state["max_turns"]:
    return "Tiden är ute! Slottet rasar samman..."
```

### 10. Gömda rum
Hemliga rum som kräver undersökning.
```python
# world.py
"bibliotek": {
    "hidden_exit": {
        "direction": "bakom_bokhyllan",
        "leads_to": "hemligt_rum",
        "requires_action": "examine bokhylla"
    }
}
```

---

## Nivå 3: Avancerat (större system)

### 11. Quest-system
Uppdrag med mål och belöningar.
```python
# world.py
QUESTS = {
    "find_crown": {
        "name": "Hitta kronan",
        "description": "Den gamla vakten vill att du hittar kungens krona.",
        "objective": "krona",
        "reward": {"gold": 100, "item": "magisk_amulett"}
    }
}

# game.py - lägg till i state
"active_quests": [],
"completed_quests": []
```

### 12. Inventory-begränsning
Max antal föremål man kan bära.
```python
# game.py
MAX_INVENTORY = 5

def pickup(item: str) -> str:
    if len(state["inventory"]) >= MAX_INVENTORY:
        return "Din ryggsäck är full! Släpp något först."
```

### 13. Kombinera föremål
Skapa nya föremål genom att kombinera.
```python
# world.py
RECIPES = {
    ("pinne", "rep"): "fiskespö",
    ("fackla", "olja"): "brinnande_fackla"
}

# server.py
@mcp.tool()
def combine(item1: str, item2: str) -> str:
    """Kombinera två föremål."""
    return game.combine_items(item1, item2)
```

### 14. Sparade spel (slots)
Flera sparplatser för olika speltillstånd.
```python
# server.py
@mcp.tool()
def save_game(slot: int) -> str:
    """Spara spelet till en slot (1-3)."""
    return game.save_to_slot(slot)

@mcp.tool()
def load_game(slot: int) -> str:
    """Ladda spel från en slot."""
    return game.load_from_slot(slot)
```

### 15. Achievements
Belöningar för att uppnå mål.
```python
# world.py
ACHIEVEMENTS = {
    "explorer": {"name": "Utforskare", "condition": "visited_all_rooms"},
    "collector": {"name": "Samlare", "condition": "collected_10_items"},
    "speedrunner": {"name": "Snabbspringare", "condition": "completed_under_50_turns"}
}

# game.py - lägg till i state
"achievements": []
```

### 16. Dynamisk värld
Rum som ändras baserat på spelarens handlingar.
```python
# world.py
"grotta": {
    "states": {
        "dark": {"description": "Det är kolmörkt. Du ser ingenting."},
        "lit": {"description": "Facklan lyser upp grottan. Du ser en trappa nedåt."}
    },
    "current_state": "dark",
    "trigger": {"use": "fackla", "changes_to": "lit"}
}
```

### 17. Multiplayer-förberedelse
Separata speltillstånd per spelare.
```python
# game.py
def load_state(player_id: str) -> dict:
    state_file = STATE_DIR / f"{player_id}.json"
    ...
```

---

## Implementation-ordning (rekommenderad)

1. **HP + Skada** - Ger spelet stakes
2. **Healing** - Balanserar skadan
3. **Examine** - Mer interaktion
4. **Fiender** - Äventyrskänsla
5. **NPCs** - Berättelse
6. **Quests** - Mål och motivation

Varje steg bygger på föregående och håller koden hanterbar.
