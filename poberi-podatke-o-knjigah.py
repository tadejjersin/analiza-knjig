import json
import re
import requests
import time
import os
import orodja
import random

json_datoteka = os.path.join("linki", "linki.json")
with open(json_datoteka, encoding="utf-8") as f:
    seznam_linkov = json.load(f)

# orodja.shrani_spletno_stran(seznam_linkov[0], "html-strani-knjig\knjiga-1")

vzorec_knjige = re.compile(
    r'<h1 id="bookTitle" class="gr-h1 gr-h1--serif" itemprop="name">\s*(?P<naslov>.*?)\s*</h1>.*?'
    r'<span itemprop="name">(?P<avtor>.*?)</span>.*?'
    r'<span itemprop="ratingValue">\s*(?P<ocena>\d\.\d\d)\s*</span>.*?'
    r'<meta itemprop="ratingCount" content="(?P<stevilo_ocen>\d+)" />.*?'
    r'<meta itemprop="reviewCount" content="(?P<stevilo_mnenj>\d+)" />.*?'
    r'<div id="description" class="readable stacked" style="right:0">(?P<opis>.*?)</div>.*?'
    r'<span itemprop="numberOfPages">(?P<stevilo_strani>\d+) pages</span>.*?'
    r'<nobr class="greyText">\s*\(first published .*?(?P<leto_izdaje>\d+)\)\s*</nobr>.*?'
    r'<a class="actionLinkLite bookPageGenreLink" href=".*?">(?P<zanr1>.*?)</a>.*?'
    r'<a class="actionLinkLite bookPageGenreLink" href=".*?">(?P<zanr2>.*?)</a>.*?'
    r'<a class="actionLinkLite bookPageGenreLink" href=".*?">(?P<zanr3>.*?)</a>',
    flags=re.DOTALL
)

vzorec_knjige2 = re.compile(
    r'{"@type":"AggregateRating","ratingValue":(?P<ocena>\d\.\d\d?),"ratingCount":(?P<stevilo_ocen>\d+),"reviewCount":(?P<stevilo_mnenj>\d+)}.*?'
    r'data-testid="bookTitle" aria-label="Book title: (?P<naslov>.*?)">.*?'
    r'class="ContributorLink__name" data-testid="name">(?P<avtor>.*?)</span>.*?'
    r'class="DetailsLayoutRightParagraph__widthConstrained"><span class="Formatted">(?P<opis>.*?)</span>.*?'
    r'<span class="Text Text__body3 Text__subdued">Genres</span>.*?'
    r'<span class="Button__labelItem">(?P<zanr1>.*?)</span>.*?'
    r'<span class="Button__labelItem">(?P<zanr2>.*?)</span>.*?'
    r'<span class="Button__labelItem">(?P<zanr3>.*?)</span>.*?'
    r'<p data-testid="pagesFormat">(?P<stevilo_strani>\d+) pages.*?'
    r'<p data-testid="publicationInfo">First published .*?(?P<leto_izdaje>\d+)</p>',
    flags=re.DOTALL
)

vzorec_opisa1 = re.compile(
    r'<span id="freeTextContainer\d+">(?P<opis>.*?)</span>',
    flags=re.DOTALL
)

vzorec_opisa2 = re.compile(
    r'<span id="freeText\d+" style="display:none">(?P<opis>.*?)</span>',
    flags=re.DOTALL
)

def polepsaj_opis(opis: str):
    vzorec_povezave = re.compile(r'<a href=".*?>')
    znaki = vzorec_povezave.findall(opis) + ["\n", "<p>", "</p>", "<i>", "</i>", "<b>", "</b>", "<u>", "</u>", "<br />", "</a>", "<em>", "</em>"]
    for znak in znaki:
        opis = opis.replace(znak, "")
    return opis
    

def izloci_podatke(vsebina, i):
    try:
        knjiga = vzorec_knjige.search(vsebina).groupdict()
        try:
            opis = vzorec_opisa2.search(knjiga["opis"]).group("opis")
        except:
            opis = vzorec_opisa1.search(knjiga["opis"]).group("opis")
        knjiga["opis"] = opis
    except:
        try:
            knjiga = vzorec_knjige2.search(vsebina).groupdict()
        except:
            return
    knjiga["naslov"] = knjiga["naslov"].replace("&#x27;", "'")
    knjiga["ocena"] = float(knjiga["ocena"])
    knjiga["stevilo_ocen"] = int(knjiga["stevilo_ocen"])
    knjiga["stevilo_mnenj"] = int(knjiga["stevilo_mnenj"])
    knjiga["stevilo_strani"] = int(knjiga["stevilo_strani"])
    knjiga["leto_izdaje"] = int(knjiga["leto_izdaje"])
    knjiga["zanri"] = [knjiga.pop(f"zanr{i}") for i in [1, 2, 3]]
    knjiga["opis"] = polepsaj_opis(knjiga["opis"])
    knjiga["id"] = i
    return knjiga

def izloci_zanre_in_opise(knjige):
    opisi, zanri = [], []

    for knjiga in knjige:
        opisi.append({"id": knjiga["id"], "opis": knjiga.pop("opis")})
        for zanr in knjiga.pop("zanri"):
            zanri.append({"id": knjiga["id"], "zanr": zanr})
    return opisi, zanri
    
knjige = []
for i, url in enumerate(seznam_linkov):
    if i >= 100:
        break
    ime_datoteke = os.path.join("html-strani-knjig", f"knjiga-{i+1}")
    if not orodja.shrani_spletno_stran(url, ime_datoteke):
        time.sleep(random.random() * 3 + 1)
    vsebina = orodja.vsebina_datoteke(ime_datoteke)
    knjiga = izloci_podatke(vsebina, i)
    if knjiga:
        knjige.append(knjiga)
ime_json = os.path.join("obdelani-podatki", "knjige.json")
orodja.zapisi_json(knjige, ime_json)
opisi, zanri = izloci_zanre_in_opise(knjige)

orodja.zapisi_csv(
    knjige, 
    ['id', 'naslov', 'avtor', 'ocena', 'stevilo_ocen', 'stevilo_mnenj', 'leto_izdaje', 'stevilo_strani'], 
    os.path.join("obdelani-podatki", "knjige.csv")
)

orodja.zapisi_csv(zanri, ['id', 'zanr'], os.path.join("obdelani-podatki", "zanri.csv"))
orodja.zapisi_csv(opisi, ['id', 'opis'], os.path.join("obdelani-podatki", "opisi.csv"))
