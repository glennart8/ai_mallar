# Simple Agent

En AI-agent som planerar och utför uppgifter steg-för-steg.

## Koncept

Agenten följer en loop:
1. TÄNK - Analysera nuvarande tillstånd
2. AGERA - Välj och kör ett verktyg
3. OBSERVERA - Notera resultatet
4. Upprepa tills uppgiften är klar

## Användning

```python
# Definiera verktyg
def my_tool(param: str) -> str:
    return "result"

TOOLS = {"my_tool": my_tool}

# Kör agenten
result = run_agent("Utför denna uppgift")
```

## När använda

- Komplexa uppgifter som kräver flera steg
- Automatisering av arbetsflöden
- Uppgifter där planen inte är känd i förväg
- Integration av flera system

## Anpassningar

- Lägg till fler verktyg i TOOLS-dictionaryn
- Ändra max_steps för längre/kortare kedjor
- Förbättra prompt för bättre resonemang
- Lägg till felhantering och loggning

## Viktiga delar

- Verktyg är vanliga Python-funktioner
- Agenten väljer själv vilka verktyg att använda
- Kontexten byggs upp steg för steg
- DONE-kommandot avslutar loopen
