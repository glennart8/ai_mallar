"""
Textäventyr - Spellogik och state-hantering.
Demonstrerar hur MCP kan använda persistent state (Resources).
"""

import json
from pathlib import Path

STATE_FILE = Path(__file__).parent / "game_state.json"

# Spelvärlden - rum och kopplingar
ROOMS = {
    "start": {
        "name": "Skogsgläntan",
        "description": "Du står i en solig skogsglänta. Fåglar kvittrar.",
        "exits": {"norr": "grotta", "öster": "flod"},
        "items": ["pinne"]
    },
    "grotta": {
        "name": "Mörk grotta",
        "description": "En fuktig grotta. Du hör droppande vatten.",
        "exits": {"söder": "start", "ner": "skatt"},
        "items": ["fackla"]
    },
    "flod": {
        "name": "Vid floden",
        "description": "En forsande flod blockerar vägen.",
        "exits": {"väster": "start", "över": "ö"},
        "items": ["rep"]
    },
    "skatt": {
        "name": "Skattkammaren",
        "description": "En glittrande kammare full av guld!",
        "exits": {"upp": "grotta"},
        "items": ["guldmynt", "krona"],
        "requires": "fackla"
    },
    "ö": {
        "name": "Den mystiska ön",
        "description": "En liten ö mitt i floden. Ett gammalt träd växer här.",
        "exits": {"tillbaka": "flod"},
        "items": ["magisk_sten"],
        "requires": "rep"
    }
}

DEFAULT_STATE = {
    "current_room": "start",
    "inventory": [],
    "hp": 100,
    "visited_rooms": ["start"]
}


def load_state() -> dict:
    """Laddar spelstate från fil, eller skapar nytt."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return DEFAULT_STATE.copy()


def save_state(state: dict):
    """Sparar spelstate till fil."""
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def get_room_info() -> str:
    """Returnerar info om nuvarande rum (RESOURCE)."""
    state = load_state()
    room_id = state["current_room"]
    room = ROOMS[room_id]

    lines = [
        f"{room['name']}",
        room['description'],
    ]

    # Visa föremål som inte plockats upp
    available_items = [i for i in room.get("items", []) if i not in state["inventory"]]
    if available_items:
        lines.append(f"Du ser: {', '.join(available_items)}")

    exits = ", ".join(room["exits"].keys())
    lines.append(f"Utgångar: {exits}")

    return "\n".join(lines)


def get_inventory() -> str:
    """Returnerar spelarens inventory (RESOURCE)."""
    state = load_state()
    if not state["inventory"]:
        return "Din ryggsäck är tom."
    return "Ryggsäck: " + ", ".join(state["inventory"])


def get_status() -> str:
    """Returnerar spelarens status (RESOURCE)."""
    state = load_state()
    return f"HP: {state['hp']} | Besökta rum: {len(state['visited_rooms'])}/{len(ROOMS)}"


def move(direction: str) -> str:
    """Flyttar spelaren i en riktning (TOOL)."""
    state = load_state()
    room = ROOMS[state["current_room"]]

    if direction not in room["exits"]:
        available = ", ".join(room["exits"].keys())
        return f"Du kan inte gå '{direction}'. Tillgängliga: {available}"

    new_room_id = room["exits"][direction]
    new_room = ROOMS[new_room_id]

    # Kolla om rummet kräver ett föremål
    if new_room.get("requires"):
        required = new_room["requires"]
        if required not in state["inventory"]:
            return f"Du behöver '{required}' för att ta dig dit."

    state["current_room"] = new_room_id
    if new_room_id not in state["visited_rooms"]:
        state["visited_rooms"].append(new_room_id)

    save_state(state)
    return get_room_info()


def pickup(item: str) -> str:
    """Plockar upp ett föremål (TOOL)."""
    state = load_state()
    room = ROOMS[state["current_room"]]
    available_items = [i for i in room.get("items", []) if i not in state["inventory"]]

    if item not in available_items:
        return f"Det finns ingen '{item}' här."

    state["inventory"].append(item)
    save_state(state)

    return f"Du plockar upp '{item}'!"


def reset_game() -> str:
    """Återställer spelet (TOOL)."""
    save_state(DEFAULT_STATE.copy())
    return "Spelet återställt! " + get_room_info()
