"""
Validerings-schema för bidragsansökan.
Anpassa fälten efter ditt formulär.
"""

SCHEMA = {
    "namn": {
        "required": True,
        "description": "Sökandes för- och efternamn"
    },
    "organisation": {
        "required": True,
        "description": "Organisation eller förening"
    },
    "organisationsnummer": {
        "required": True,
        "format": "XXXXXX-XXXX (6 siffror, bindestreck, 4 siffror)"
    },
    "email": {
        "required": True,
        "format": "Giltig e-postadress"
    },
    "telefon": {
        "required": False,
        "format": "Telefonnummer"
    },
    "projektnamn": {
        "required": True,
        "description": "Namn på projektet"
    },
    "projektbeskrivning": {
        "required": True,
        "min_length": 100,
        "description": "Beskrivning av projektet (minst 100 tecken)"
    },
    "budget": {
        "required": True,
        "format": "Numeriskt värde i kronor"
    },
    "sokt_belopp": {
        "required": True,
        "format": "Numeriskt värde i kronor"
    }
}
