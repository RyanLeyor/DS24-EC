Här är min lösning på kunskapskontroll 1 i kursen Fördjupning i Pythonprogrammering

# Filstruktur:

Kunskapskontroll Fördjupning Python/
util/
    util.py #För loggers, OBS: util.util i koder syftar på detta struktur.

main.py #Huvudflödet - Läser in CSV fil och uppdaterar SQLite databas
test_weather.py # För att köra automatiska tester
weather.csv # Indata fil 

# För att köra projektet
# kör följande i teminalen:  
    python main.py

# Utföra tester: (Genom Pytest)
pytest -q # om detta inte fungerar, testa python -m pytest -q  för att köra pytest via python.

# Schemaläggning:
Följande flöde kan schemaläggas för automatisk körning via Windows: Schemaläggare och Mac/Linux: CRON. För att automatiskt lagra vädret för städerna Stockholm, Göteborg och Malmö. 


