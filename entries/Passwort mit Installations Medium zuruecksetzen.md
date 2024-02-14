# Passwort mit Installations Medium zuruecksetzen

Alle Windows-Benutzer sichern ihren Computer mit einem Passwortschutz. Dies ist eine notwendige Massnahme, da jemand auf Windows zugreifen und die Daten ohne Ihre Erlaubnis ausnutzen oder missbrauchen koennte. Aber es ist moeglich, dass Sie das Passwort vergessen und auf dem Anmeldebildschirm feststecken.

Wie knacken Sie Windows 11/10 Passwort, wenn Sie es vergessen haben? In diesem Artikel besprechen wir das.

Teil 1. Per Installationsdatentraeger knacken
Teil 2. PC Zuruecksetzen
Teil 3. Ein anderen Administrator verwenden

### Teil 1. Per Installationsdatentraeger knacken

Wie knackt man das Windows 10 Passwort? Bei dieser Methode benoetigen Sie einen Installationsdatentraeger, der ein USB-Stick oder eine CD/DVD sein kann, beides funktioniert. Ein Installationsdatentraeger ist ein bootfaehiger Windows-Datentraeger. Mit diesem Windows-Installationsdatentraeger koennen Sie das vergessene Windows 11/10-Passwort knacken. Fuehren Sie die folgenden Schritte aus:

Schritt 1: Starten Sie Ihren Computer neu waehrend die Installationsdiskette eingelegt ist.
Schritt 2: Wenn Sie eine CD/DVD als Installationsmedium verwenden, stellen Sie Ihren PC in den BIOS-Einstellungen so ein, dass er von CD/DVD bootet, oder wenn Sie ein USB-Laufwerk als

Installationsmedium verwenden, stellen Sie Ihren PC so ein, dass er von USB bootet.
Schritt 3: Starten Sie nun Ihren Computer neu und starten Sie die Windows 10-Installation.

Schritt 4: Nun muessen Sie die Eingabeaufforderung oeffnen. Druecken Sie dazu "Umschalt" + "F10".

Schritt 5: Geben Sie folgende Befehle ein:

     D: 
     cd Windows\System32 
     ren sethc.exe sethc.exe.bak 
     copy cmd.exe sethc.exe	
     



#### Hinweis: 
"D:" ist das Laufwerk, auf dem Ihr Windows installiert ist. Wenn Sie Windows in einem anderen Laufwerk installiert haben, koewnnen Sie den Buchstaben aendern.

Schritt 6: Schliessen Sie die Eingabeaufforderung. Brechen Sie die Installation von Windows ab. Starten Sie Ihren PC neu, ohne den Installationsdatentraeger einzulegen.


Schritt 7: Druecken Sie auf Ihrem Anmeldebildschirm 5 Mal die Umschalttaste. Die Eingabeaufforderung mit Administratorrechten wird geoeffnet.


Schritt 8: Hier koennen Sie das Passwort fuer Ihr Benutzerkonto aendern. Geben Sie net user ein, um alle Benutzerkonten aufzulisten. Um nun das Passwort zu aendern, geben Sie  net user user_name new_password. In diesem Fall ist user_name ein bestimmtes Benutzerkonto.

Schritt 9: Jetzt koennen Sie sich bei Windows 10 mit dem neuen Passwort anmelden, das Sie fuer das Benutzerkonto festgelegt haben.