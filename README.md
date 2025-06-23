# PhotoMemory
PhotoMemory je web aplikacija koja prikazuje fotografe i informacije o njima. Može biti korisna korisnica koji trebaju unajmiti fotografa za neki događaj. Korisnik može gledati listu fotografa i filtrirati ih kako mu odgovara. Može filtrirati po gradu, trenutnoj dostupnosti fotografa i po maksimalnoj cijeni koju si korisnik može priuštiti. Ukoliko je korisnik sam fotograf ili poznaje nekog fotografe može dodati novog fotografa u listu te isto tako ažurirati fotografe ukoliko je došlo do neke greške ili su se informacije promijenile te izbrisati fotografe ako više ne rade. Korisnik također može pogledati graf koji pokazuje prosječnu cijenu po satu u eurima fotografa po gradovima te tako može vidjeti gdje su fotografi općenito jefntiniji ili skuplji.

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
