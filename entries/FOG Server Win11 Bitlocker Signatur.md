# FOG Server Win11 Bitlocker Signatur

Da aus mir nicht verstaendlichen Gruenden Win11 ungefragt bei einer Installation mit Bitlocker verschluesselt
kann es beim Image Ziehen Probleme geben.

#### Loesung

CMD als Adminitrator ausfuehren und folgendes eingeben:

 ```` manage-bde -off C: ````

damit wird dann wieder Entschluesselt

#### Tipp !

Da nicht angezeigt wird ob er Fertig ist empfiehlt sich hin und wieder den Status abzurufen.
Dieses macht man folgendermassen:

   ````manage-bde -status C:````

Erst wenn der Status sagt ja 0% zu entschluesseln und auch das Protokoll, womit verschluesselt wurde, weg ist kann man den Rechner neustarten und mit FOG Server sich das Image ziehen