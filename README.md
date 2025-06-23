# PhotoMemory
PhotoMemory je web aplikacija koja prikazuje fotografe i informacije o njima. Može biti korisna korisnica koji trebaju unajmiti fotografa za neki događaj.

## Funkcionalnosti
1. Pregled fotografa i njihovih informacija
2. Dodavanje novih fotografa
3. Brisanje fotografa
4. Ažuriranje fotografa
5. Filtriranje fotografa po gradu
6. Filtriranje fotografa po dostupnosti
7. Filtriranje fotografa po maksimalnoj cijeni koju odredi korisnik
8. Prikazuje graf koji pokazuje prosječnu cijenu po satu u eurima za različite gradove u kojima fotografi rade

## Instalacija
1. Instalirajte Docker Desktop i Git
2. Otvorite terminal i pokrenite git clone https://github.com/LG-202003/Projekt-Informacijski-Sustavi-PhotoMemory
3. cd Projekt-Informacijski-Sustavi-PhotoMemory
4. Pokrenuti Docker: docker build -t photomemory
5. docker run -p 5001:8080 photomemory
