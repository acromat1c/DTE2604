# Programmeringskurs
IT bedriften Morild Data BA har fått i oppdrag fra utdanningsinstitusjonen KnowItAll å utvikle et system som skal gjøre det morsomt og enkelt å lære programmering og videreutvikle ferdighetene. Systemet skal være spill-basert med ulike nivåer, oppgraderinger og belønninger.

## Installasjonsveiledning
Koden til prosjektet er på Github. Det er 2 viktige brancher å vite om, main branch er for kode som er testet og virker lokalt. Det er en annen branch som heter ‘docker-server’ som brukes når man vil installere programmet på en server. Den har litt andre innstillinger som bruker MariaDB istedenfor Sqlite, der man må bruke en .env fil istedenfor at innstillinger og passord er lagret innenfor kildekoden til programmet. 
### For å installere og kjøre lokalt på egen pc (for testing og utvikling):
1.	Last ned og gå inn i mappen til prosjektet
2.	Kjør setup.py
3.	Når setup.py spør om å kjøre Django server, skriv ‘y’
4.	Serveren kjører på localhost:8000

Kommandoer:
```
git clone https://github.com/acromat1c/DTE2604 && cd DTE2604/
python3 setup.py
```

### For å installere på en server:
1.	Last ned og gå inn i mappen til prosjektet
2.	Bytt til docker-server branch
3.	Lag en fil men navn .env. Den må inneholde variablene DJANGO_SECRET_KEY, DEBUG, DJANGO_ALLOWED_HOSTS, og DJANGO_CSRF_TRUSTED.
4.	Lag Docker image
5.	Push image til systemet du bruker (eks. gcloud)
6.	Konfigurer cloud platformen til å bruke din docker image, og koble den til en MariaDB database.
7.	Log inn på serveren sin terminal og kjør migrate og loaddata
8.	Nettsiden er nå klar for å brukes.

Kommandoer:
```
På egen maskin:
git clone https://github.com/acromat1c/DTE2604 && cd DTE2604/
git checkout docker-server
docker compose create
docker push [link]
```

På serveren:
```
python3 manage.py migrate
python3 manage.py loaddata fixtures/*
```
