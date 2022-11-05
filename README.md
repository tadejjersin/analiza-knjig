# Analiza knjig 
Analiziral bom podatke iz spletne strani goodreads.com, natančneje iz seznama "Books That Everyone Should Read At Least Once" (https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once). 

O vsaki knjigi bom zajel podatke o naslovu, avtorju, opisu, letu izdaje, številu strani, žanrih, oceni na spletni strani, številu ocen in številu mnenj. Zajetih podatkov naj bi bilo 5000, a jih je manj zaradi ponavljajočih knjig(ne seznamu so lahko iste knjige, a z drugimi izdajami) in, ker je surov html dobljen z requests.get včasih "pokvarjen".

## Hipoteze
- Najbolje ocenjene knjige bodo klasike
- Ali kakšni žanri dobivajo bistveno boljše ocene kot ostali?
- Ali dolžina knjige vpliva na oceno?
