API
Mitt program följer ett flerstegs-API-flöde med token-autentisering.

#Funktion

Programmet arbetar som följande:

Skickar en POST-request för att hämta en token
Använder token i en Authorization-header
Verifierar token via API:t
Skickar vidare verifierad data för att hämta ett slutligt svar (flag)
Tekniker som används:
Python
requests-biblioteket
HTTP (GET / POST)
JSON
Felhantering med try/except
För att testa programmet:
Installera bibliotek/verktyg: pip install requests
Kör programmet i din terminal: python laboration1.py