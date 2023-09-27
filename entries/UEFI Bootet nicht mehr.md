
# Methode 1

### GPT (UEFI) Bootmenü Reparatur mit der Recovery DVD oder Installations-DVD

-   **Wichtig:** Alle anderen Festplatten einmal abziehen, sodass nur die Systemplatte angeschlossen ist.
-   Die erstellten [Recovery](https://www.deskmodder.de/wiki/index.php?title=Windows_10_sichern_Sicherung_Backup_erstellen_und_wiederherstellen#Wiederherstellungslaufwerk_Recovery_erstellen "Windows 10 sichern Sicherung Backup erstellen und wiederherstellen") oder die Installations-DVD ins Laufwerk schieben und von der DVD starten.
-   Wenn bei der Installation diese Auswahl erscheint (siehe Bild), dann unten links auf Computerreparatur klicken.
-   Nun gelangt man in die [Erweiterte Startoptionen von Windows 10](https://www.deskmodder.de/wiki/index.php?title=Erweiterte_Startoptionen_von_Windows_10_aufrufen_und_starten "Erweiterte Startoptionen von Windows 10 aufrufen und starten").
-   Hier nun die Erweiterten Optionen und dann Eingabeaufforderung anklicken.
-   In der Eingabeaufforderung nun nacheinander diese Befehle eingeben und jeweils mit Enter bestätigen:
    -   **diskpart**
    -   **list vol**
    -   **sel vol y** - _y = die Nummer der Systempartition ._
    -   **format FS="Fat32" Quick**
    -   _Der EFI-Partition (EPS) wird nun ein Laufwerksbuchstabe zuweisen_
    -   **assign letter=Z:** _(Falls der Laufwerksbuchstabe vergeben ist, einen anderen nutzen)._
    -   **exit**

Jetzt sind wir wieder in der Eingabeaufforderung und können die UEFI-Bootpartition reparieren.

-   In der Eingabeaufforderung nun
    -   **bcdboot c:\Windows /l de-de /s Z: /f UEFI** und Enter drücken für die Reparatur. _c: = Startpartition, muss eventuell angepasst werden._ - _Auch hier ist der Laufwerksbuchstabe Z mit eurem Laufwerksbuchstaben zu ersetzten._

Sollte das nicht funktionieren:

Backup der c: Windows Partition erstellen und Win11 neu installieren. Danach Backup wieder zurückspielen.

