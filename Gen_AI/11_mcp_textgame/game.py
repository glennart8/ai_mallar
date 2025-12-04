"""
Textäventyr - Spellogik och state-hantering.
Demonstrerar hur MCP kan använda persistent state (Resources).
"""

import json
from pathlib import Path
from world import LEVELS, DEFAULT_STATE

STATE_FILE = Path(__file__).parent / "game_state.json"


def load_state() -> dict:
    """Laddar spelstate från fil, eller skapar nytt."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return DEFAULT_STATE.copy()


def save_state(state: dict):
    """Sparar spelstate till fil."""
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def get_rooms(state: dict) -> dict:
    """Hämtar rummen för nuvarande nivå."""
    return LEVELS[state["current_level"]]["rooms"]


def get_level_info(state: dict) -> dict:
    """Hämtar info om nuvarande nivå."""
    return LEVELS[state["current_level"]]


def get_room_info() -> str:
    """Returnerar info om nuvarande rum (RESOURCE)."""
    state = load_state()
    rooms = get_rooms(state)
    level = get_level_info(state)
    room_id = state["current_room"]
    room = rooms[room_id]

    lines = [
        f"[{level['name']}] {room['name']}",
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
    level = get_level_info(state)
    rooms = get_rooms(state)
    return f"Nivå: {state['current_level']} ({level['name']}) | HP: {state['hp']} | Rum: {len(state['visited_rooms'])}/{len(rooms)}"


def move(direction: str) -> str:
    """Flyttar spelaren i en riktning (TOOL)."""
    state = load_state()
    rooms = get_rooms(state)
    level = get_level_info(state)
    room = rooms[state["current_room"]]

    if direction not in room["exits"]:
        available = ", ".join(room["exits"].keys())
        return f"Du kan inte gå '{direction}'. Tillgängliga: {available}"

    new_room_id = room["exits"][direction]

    # Hantera nivåbyte
    if new_room_id == "NEXT_LEVEL":
        goal_item = level["goal"]
        if goal_item not in state["inventory"]:
            return f"Portalen kräver '{goal_item}' för att aktiveras."

        next_level = state["current_level"] + 1
        if next_level not in LEVELS:
            return "GRATTIS! Du har klarat alla nivåer!"

        state["completed_levels"].append(state["current_level"])
        state["current_level"] = next_level
        state["current_room"] = "start"
        state["visited_rooms"] = ["start"]
        save_state(state)
        return f"Du klev genom portalen!\n\n=== NIVÅ {next_level}: {LEVELS[next_level]['name'].upper()} ===\n\n{get_room_info()}"

    new_room = rooms[new_room_id]

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
    rooms = get_rooms(state)
    room = rooms[state["current_room"]]
    available_items = [i for i in room.get("items", []) if i not in state["inventory"]]

    if item not in available_items:
        return f"Det finns ingen '{item}' här."

    state["inventory"].append(item)
    save_state(state)

    # Kolla om det är nivåns mål
    level = get_level_info(state)
    if item == level["goal"]:
        return f"Du plockar upp '{item}'! ✨ Detta är nyckeln till nästa nivå!"

    return f"Du plockar upp '{item}'!"


def reset_game() -> str:
    """Återställer spelet (TOOL)."""
    save_state(DEFAULT_STATE.copy())
    return "Spelet återställt! " + get_room_info()
