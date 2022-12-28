# Analiza knjig 
Analiziral bom podatke iz spletne strani goodreads.com, natančneje iz seznama "Books That Everyone Should Read At Least Once" (https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once). Seznam je narejen tako, da vsak uporabnik spletne strani goodreads.com lahko glasuje za knjige, ki so potem urejene po številu dobljenih točk. 

O vsaki knjigi bom zajel podatke o naslovu, avtorju, opisu, letu izdaje, številu strani, žanrih, oceni na spletni strani, številu ocen in številu mnenj. 

## O zajemu podatkov
Najprej poženemo datoteko poberi-linke.py, ki iz zgoraj omenjenega seznama pobere 5000 linkov (povezav) in jih zapiše v datoteko seznam-linkov.json. Nato poženemo datoteko poberi-podatke-o-knjigah.py, ki iz vsakege povezave pobere zgoraj navedene podatke za posamezno knjigo. 

Pobranih knjig je sicer manj kot 5000, ker so na seznamu lahko posamezne knjige večkrat (zaradi različnih izdaj), ter jih štejemo le enkrat in, ker so nekatere surove strani, ki jih dobimo z requests.get, "pokvarjene" in ne moremo izločiti podatkov.

Datoteka knjige.json vsebuje vse prej navedene podatke, datoteka knjige.csv vse razen opisov in žanrov, opisi.csv opise in zanri.csv žanre.

## Hipoteze
- Najbolje ocenjene knjige bodo klasike
- Ali kakšni žanri dobivajo bistveno boljše ocene kot ostali?
- Ali dolžina knjige vpliva na oceno?
- Kateri avtorji pišejo najdaljše knjige?
