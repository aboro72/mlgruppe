# Windows Server Evaluation edition nach Vollversion

Schritt 1: 

Oeffnen Sie die Befehlsaufforderung als Administrator und fuehren Sie diesen Befehl aus.

  dism /online /get-currentedition

um herrauszufinden welche Version sie haben


Schritt 2: 

Listen Sie die Versionen auf auf die Sie konvertieren koennen.
Fuehren Sie dazu den folgenden Befehl aus.

  dism /online /get-targeteditions


Schritt 3:

Konvertieren Sie Ihr Windows in die gewuenschte Version.
Fuehren Sie den Befehl unten aus, um einen Konvertierungsprozess zu starten.

  z.B.
  dism /online /set-edition:serverstandard /productkey:N69G4-B89J2-4G8F4-WWYCC-J464C /accepteula


eine liste mit Keys zur Konvertierung finden Sie unter https://learn.microsoft.com/en-us/windows-server/get-started/kms-client-activation-keys#windows-server-ltscltsb-versions
Nach Abschluss des 3. Schritts werden Sie gebeten, Ihren Server neu zu starten. Antworten Sie einfach: Y.

Somit wurde jetzt aus der Eval Version eine Vollversion. 

### Als naechstes Aktivieren Sie Ihre Serverversion mit einem Orginal Key 

Schritt 1: 

Oeffnen Sie die Befehlsaufforderung als Administrator und fuehren Sie diesen Befehl aus.

  slmgr /ipk <Ihr_product key>

Schritt 2a:

Geben Sie jetzt folgendes in die Befehlsaufforderung ein

 slmgr /ato

Schritt 2b:
Sollten Sie keinen eigenen Productkey haben geben Sie folgendes ein und lassen Schritt 1 weg
 slmgr /skms kms8.msguides.com

mache Sie nun mit Schritt2a weiter.


 
