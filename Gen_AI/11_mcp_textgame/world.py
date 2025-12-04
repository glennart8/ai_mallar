"""
Spelvärlden - rum, kopplingar och starttillstånd.
"""

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
