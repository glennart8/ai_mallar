"""
Spelvärlden - nivåer, rum, kopplingar och starttillstånd.
"""

LEVELS = {
    1: {
        "name": "Skogen",
        "goal": "magisk_sten",  # Samla detta för att låsa upp nästa nivå
        "rooms": {
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
                "description": "En liten ö mitt i floden. Ett gammalt träd växer här. En portal glimmar svagt.",
                "exits": {"tillbaka": "flod", "portal": "NEXT_LEVEL"},
                "items": ["magisk_sten"],
                "requires": "rep"
            }
        }
    },
    2: {
        "name": "Slottet",
        "goal": "krondiadem",  # Samla detta för att vinna spelet
        "rooms": {
            "start": {
                "name": "Slottsentrén",
                "description": "Du står framför ett förfallet slott. Portarna är öppna.",
                "exits": {"in": "hall"},
                "items": []
            },
            "hall": {
                "name": "Stora hallen",
                "description": "En enorm hall med damm och spindelväv. Trappor leder upp och ner.",
                "exits": {"ut": "start", "upp": "torn", "ner": "fängelse", "öster": "bibliotek"},
                "items": ["rostig_nyckel"]
            },
            "bibliotek": {
                "name": "Biblioteket",
                "description": "Böcker ligger utspridda överallt. Något glänser bakom en bokhylla.",
                "exits": {"väster": "hall"},
                "items": ["antik_karta", "hemlig_passage"],
                "requires": "rostig_nyckel"
            },
            "torn": {
                "name": "Tornet",
                "description": "Du ser hela landskapet härifrån. En kista står i hörnet.",
                "exits": {"ner": "hall"},
                "items": ["silverdolk"],
                "requires": "antik_karta"
            },
            "fängelse": {
                "name": "Fängelsehålan",
                "description": "Mörkt och fuktigt. Kedjor hänger på väggarna. En varelse rör sig i skuggorna.",
                "exits": {"upp": "hall", "djupare": "skattkammare"},
                "items": [],
                "requires": "silverdolk"
            },
            "skattkammare": {
                "name": "Slottets skattkammare",
                "description": "Guld och juveler överallt! I mitten tronar det eftersökta kronjuvelen.",
                "exits": {"tillbaka": "fängelse"},
                "items": ["krondiadem", "guldtacka"],
                "requires": "hemlig_passage"
            }
        }
    }
}

# Bakåtkompatibilitet - ROOMS pekar på level 1
ROOMS = LEVELS[1]["rooms"]

DEFAULT_STATE = {
    "current_level": 1,
    "current_room": "start",
    "inventory": [],
    "hp": 100,
    "visited_rooms": ["start"],
    "completed_levels": []
}
