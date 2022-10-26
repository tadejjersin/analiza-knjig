# https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once?page=1

import orodja
import re
import os
import time

vzorec_povezave = re.compile(
    r'<a class="bookTitle" itemprop="url" href="(?P<link>.*?)">',
    flags=re.DOTALL
)

def linki_na_strani(st_strani):
    linki = []
    zacetek_linka = 'https://www.goodreads.com'
    for i in range(1, st_strani + 1):
        time.sleep(5)
        url = f'https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once?page={i}'
        imenik = 'html-datoteke'
        ime_datoteke = f'stran-{i}'
        datoteka = os.path.join(imenik, ime_datoteke)
        orodja.shrani_spletno_stran(url, datoteka)
        vsebina = orodja.vsebina_datoteke(datoteka)
        for l in vzorec_povezave.finditer(vsebina):
            link = zacetek_linka + l.group("link")
            linki.append(link)
    return linki

def shrani_linke(imenik, json_datoteka, st_strani):
    ime_json_datoteke = os.path.join(imenik, json_datoteka)
    linki = linki_na_strani(st_strani)
    orodja.zapisi_json(linki, ime_json_datoteke)

shrani_linke("linki", "linki.json", 50)

