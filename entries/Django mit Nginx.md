# Einrichten von Django mit Postgres, Nginx und Gunicorn unter Ubuntu/Debian

Published on August 20, 2022


![Einrichten von Django mit Postgres, Nginx und Gunicorn unter Ubuntu 20.04](https://www.digitalocean.com/_next/static/media/intro-to-cloud.d49bc5f7.jpeg "Einrichten von Django mit Postgres, Nginx und Gunicorn unter Ubuntu 20.04")

### Einführung

Django ist ein leistungsfähiges Web-Framework, das Ihnen dabei helfen kann, Ihre Python-Anwendung oder Website bereitzustellen. Django umfasst einen vereinfachten Entwicklungsserver zum lokalen Testen Ihres Codes; für alles, was auch nur ansatzweise mit der Produktion zu tun hat, wird ein sicherer und leistungsfähiger Webserver benötigt.

In diesem Leitfaden zeigen wir, wie sich bestimmte Komponenten zum Unterstützen und Bereitstellen von Django-Anwendungen in Ubuntu 20.04 installieren und konfigurieren lassen. Wir werden anstelle der standardmäßigen SQLite-Datenbank eine PostgreSQL-Datenbank einrichten. Wir werden den Gunicorn-Anwendungsserver als Schnittstelle zu unseren Anwendungen konfigurieren. Dann werden wir Nginx als Reverseproxy für Gunicorn einrichten, damit wir beim Bereitstellen unserer Anwendungen auf dessen Sicherheits- und Leistungsmerkmale zugreifen können.

## Voraussetzungen und Ziele

Um diesen Leitfaden erfolgreich zu absolvieren, sollten Sie eine neue Ubuntu 20.04-Serverinstanz mit einer einfachen Firewall und einem Nicht-root-Benutzer mit `sudo`-Berechtigungen konfiguriert haben. In unserem [Leitfaden zur Ersteinrichtung des Servers](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-20-04) erfahren Sie, wie Sie die Einrichtung vornehmen.

Wir werden Django in einer virtuellen Umgebung installieren. Wenn Sie Django in einer für Ihr Projekt spezifischen Umgebung installieren, können Sie Ihre Projekte und deren Anforderungen separat verwalten.

Sobald wir über unsere Datenbank verfügen und die Anwendung ausgeführt wird, installieren und konfigurieren wir den Gunicorn-Anwendungsserver. Dieser wird als Schnittstelle zu unserer Anwendung dienen und Clientanfragen aus HTTP in Python-Aufrufe übersetzen, die unsere Anwendung verarbeiten kann. Dann richten wir Nginx vor Gunicorn ein, um dessen leistungsfähige Verbindungsverwaltungsmechanismen und einfach zu implementierenden Sicherheitsfunktionen nutzen zu können.

Fangen wir an.

## Installieren der Pakete aus den Ubuntu-Repositorys

Zu Beginn laden wir alle Elemente, die wir benötigen, aus den Ubuntu-Repositorys herunter und installieren sie. Ein wenig später werden wir mit dem Python-Paketmanager `pip` zusätzliche Komponenten installieren.

Wir müssen zuerst den lokalen Paketindex `apt` aktualisieren und dann die Pakete herunterladen und installieren: Die installierten Pakete hängen davon ab, welche Version von Python Sie für Ihr Projekt verwenden werden.

Wenn Sie Django mit **Python 3** nutzen, geben Sie Folgendes ein:

```
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl

```

Django 1.11 ist die letzte Version von Django, die Python 2 unterstützt. Wenn Sie neue Projekte starten, wird dringend empfohlen, Python 3 zu wählen. Wenn Sie **Python 2** weiter verwenden müssen, geben Sie Folgendes ein:

```
sudo apt update
sudo apt install python-pip python-dev libpq-dev postgresql postgresql-contrib nginx curl

```

Dadurch werden `pip`, die Python-Entwicklungsdateien, die zum späteren Erstellen von Gunicorn benötigt werden, das Postgres-Datenbankysystem, die zum Interagieren damit erforderlichen Bibliotheken sowie der Nginx-Webserver installiert.

## Erstellen der PostgreSQL-Datenbank und des Benutzers

Wir legen sofort los und erstellen für unsere Django-Anwendung eine Datenbank und einen Datenbankbenutzer.

Standardmäßig nutzt Postgres ein Authentifizierungschema namens „Peer Authentication“ für lokale Verbindungen. Im Grunde bedeutet dies, dass sich der Benutzer ohne weitere Authentifizierung anmelden kann, wenn der Benutzername des Benutzers im Betriebssystem mit einem gültigen Postgres-Benutzernamen übereinstimmt.

Während der Postgres-Installation wurde ein Betriebssystembenutzer namens `postgres` erstellt, der dem administrativen PostgreSQL-Benutzer `postgres` entspricht. Wir benötigen diesen Benutzer zur Erledigung administrativer Aufgaben. Wir können sudo verwenden und den Benutzernamen mit der Option `-u` übergeben.

Melden Sie sich in einer interaktiven Postgres-Sitzung an, indem Sie Folgendes eingeben:

```
sudo -u postgres psql

```

Ihnen wird eine PostgreSQL-Eingabeaufforderung angezeigt, in der Sie Ihre Anforderungen einrichten können.

Erstellen Sie zunächst eine Datenbank für Ihr Projekt:

```
CREATE DATABASE myproject;

```

**Anmerkung:** Jede Postgres-Anweisung muss mit einem Semikolon enden; stellen Sie sicher, dass Ihr Befehl auf ein Semikolon endet, falls Probleme auftreten.

Erstellen Sie als Nächstes einen Datenbankbenutzer für das Projekt. Wählen Sie unbedingt ein sicheres Passwort:

```
CREATE USER myprojectuser WITH PASSWORD 'password';

```

Anschließend ändern wir einige der Verbindungsparameter für den gerade erstellten Benutzer. Dadurch werden Datenbankoperationen beschleunigt, sodass die richtigen Werte nicht jedes Mal abgefragt und festgelegt werden müssen, wenn eine Verbindung hergestellt wird.

Wir legen die Standardkodierung auf `UTF-8` fest, was Django erwartet. Außerdem legen wir das standardmäßige Transaktionsisolierungsschema auf „read committed“ fest, um das Lesen von Blöcken aus Transaktionen ohne Commit zu blockieren. Schließlich legen wir die Zeitzone fest. Standardmäßig werden unsere Django-Projekte die Zeitzone `UTC` verwenden. Dies sind alles Empfehlungen aus [dem Django-Projekt selbst](https://docs.djangoproject.com/en/3.0/ref/databases/#optimizing-postgresql-s-configuration):

```
ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myprojectuser SET timezone TO 'UTC';

```

Jetzt können wir unserem neuen Benutzer Zugriff zum Verwalten unserer neuen Datenbank gewähren:

```
GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;

```

Wenn Sie damit fertig sind, beenden Sie die PostgreSQL-Eingabeaufforderung durch folgende Eingabe:

```
\q

```

Postgres ist nun so eingerichtet, dass Django eine Verbindung herstellen und dessen Datenbankinformationen verwalten kann.

## Erstellen einer virtuellen Python-Umgebung für Ihr Projekt

Nachdem wir unsere Datenbank erstellt haben, können wir nun damit beginnen, die restlichen Projektanforderungen zu erfüllen. Wir werden unsere Python-Anforderungen zur einfacheren Verwaltung in einer virtuellen Umgebung installieren.

Dazu benötigen wir zunächst Zugriff auf den Befehl `virtualenv`. Wir können ihn mit `pip` installieren.

Wenn Sie **Python 3** verwenden, aktualisieren Sie `pip` und installieren Sie das Paket durch folgende Eingabe:

```
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv

```

Wenn Sie **Python 2** verwenden, aktualisieren Sie `pip` und installieren Sie das Paket durch folgende Eingabe:

```
sudo -H pip install --upgrade pip
sudo -H pip install virtualenv

```

Nach der Installation von `virtualenv` können wir mit der Gestaltung unseres Projekts beginnen. Erstellen und wechseln Sie in ein Verzeichnis, in dem wir unsere Projektdateien speichern können.

```
mkdir ~/myprojectdir
cd ~/myprojectdir

```

Erstellen Sie im Projektverzeichnis durch folgende Eingabe eine virtuelle Python-Umgebung:

```
virtualenv myprojectenv

```

Auf diese Weise wird ein Verzeichnis mit dem Namen `myprojectenv` in Ihrem Verzeichnis `myprojectdir` erstellt. Darin wird eine lokale Version von Python und eine lokale Version von `pip` installiert. Mit ihrer Hilfe können wir für unser Projekt eine isolierte Python-Umgebung installieren und konfigurieren.

Bevor wir die Python-Anforderungen unseres Projekts installieren, müssen wir die virtuelle Umgebung aktivieren. Geben Sie hierzu Folgendes ein:

```
source myprojectenv/bin/activate

```

Ihre Eingabeaufforderung ändert sich und zeigt an, dass Sie jetzt innerhalb einer virtuellen Python-Umgebung arbeiten. Sie sieht etwa wie folgt aus: `(myprojectenv)user@host:~/myprojectdir$`.

Bei aktivierter virtueller Umgebung installieren Sie Django, Gunicorn und den PostgreSQL-Adapter `psycopg2` mit der lokalen Instanz von `pip`:

**Anmerkung:** Wenn die virtuelle Umgebung aktiviert ist (wenn Ihrer Eingabeaufforderung `(myprojectenv)` voransteht), verwenden Sie `pip` anstelle von `pip3`, selbst wenn Sie Python 3 verwenden. Die Kopie des Tools der virtuellen Umgebung heißt immer `pip` – unabhängig von der Python-Version.

```
pip install django gunicorn psycopg2-binary

```

Sie sollten nun die gesamte für den Start eines Django-Projekts erforderliche Software haben.

## Erstellen und Konfigurieren eines neuen Django-Projekts

Nach der Installation unserer Python-Komponenten können wir die eigentlichen Django-Projektdateien erstellen.

### Erstellen des Django-Projekts

Da wir bereits über ein Projektverzeichnis verfügen, werden wir Django anweisen, die Dateien dort zu installieren. Es wird ein Verzeichnis der zweiten Ebene mit dem tatsächlichen Code erstellt, was normal ist, und ein Managementskript in diesem Verzeichnis platziert. Der Schlüssel dazu besteht darin, dass wir das Verzeichnis explizit definieren, anstatt Django Entscheidungen in Bezug auf unser aktuelles Verzeichnis zu ermöglichen:

```
django-admin.py startproject myproject ~/myprojectdir

```

An diesem Punkt sollte Ihr Projektverzeichnis (in unserem Fall `~/myprojectdir`) folgenden Inhalt haben:

-   `~/myprojectdir/manage.py`: Ein Django-Projektmanagement-Skript.
-   `~/myprojectdir/myproject/`: Das Django-Projektpaket. Dieses sollte die Dateien `__init__.py`, `settings.py`, `urls.py`, `asgi.py` und `wsgi.py` enthalten.
-   `~/myprojectdir/myprojectenv/`: Das Verzeichnis der virtuellen Umgebung, die wir zuvor erstellt haben.

### Anpassen der Projekteinstellungen

Das Erste, was wir mit unseren neu erstellten Projektdateien tun sollten, ist das Anpassen der Einstellungen. Öffnen Sie die Einstellungsdatei in Ihrem Texteditor:

```
nano ~/myprojectdir/myproject/settings.py

```

Suchen Sie zunächst nach der Direktive `ALLOWED_HOSTS`. Dadurch wird eine Liste der Adressen oder Domänennamen des Servers definiert, die zum Herstellen einer Verbindung mit der Django-Instanz genutzt werden können. Alle eingehenden Anfragen mit einem **Host**, der sich nicht in dieser Liste befindet, werden eine Ausnahme auslösen. Django verlangt, dass Sie dies so festlegen, um eine bestimmte Art von Sicherheitslücke zu verhindern.

In den quadratischen Klammern listen Sie die IP-Adressen oder Domänennamen auf, die mit Ihrem Django-Projekt verknüpft sind. Jedes Element sollte in Anführungszeichen aufgelistet werden, wobei Einträge durch ein Komma getrennt werden. Wenn Sie Anfragen für eine ganze Domäne und Subdomänen wünschen, stellen Sie dem Anfang des Eintrags einen Punkt voran. Im folgenden Snippet befinden sich einige auskommentierte Beispiele:

**Anmerkung:** Stellen Sie sicher, dass `localhost` als eine der Optionen eingeschlossen ist, da wir Verbindungen über eine lokale Nginx-Instanz vermitteln werden.

~/myprojectdir/myproject/settings.py

```
. . .
# The simplest case: just add the domain name(s) and IP addresses of your Django server
# ALLOWED_HOSTS = [ 'example.com', '203.0.113.5']
# To respond to 'example.com' and any subdomains, start the domain with a dot
# ALLOWED_HOSTS = ['.example.com', '203.0.113.5']
ALLOWED_HOSTS = ['your_server_domain_or_IP', 'second_domain_or_IP', . . ., 'localhost']
```

Als Nächstes suchen Sie nach dem Bereich, der Datenbankzugriff konfiguriert. Er beginnt mit `DATABASES`. Die Konfiguration in der Datei dient für eine SQLite-Datenbank. Wir haben für unser Projekt bereits eine PostgreSQL-Datenbank erstellt; daher müssen wir die Einstellungen anpassen.

Ändern Sie die Einstellungen mit Ihren PostgreSQL-Datenbankinformationen. Wir weisen Django an, den mit `pip` installierten `psycopg2`-Adapter zu verwenden. Wir müssen den Datenbanknamen, den Namen des Datenbankbenutzers und das Passwort des Datenbankbenutzers angeben. Dann geben wir an, dass sich die Datenbank auf dem lokalen Computer befindet. Sie können die `PORT`-Einstellung als leere Zeichenfolge belassen:

~/myprojectdir/myproject/settings.py

```
. . .

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myproject',
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

. . .
```

Als Nächstes bewegen Sie sich nach unten zum Ende der Datei und fügen eine Einstellung hinzu, die angibt, wo die statischen Dateien platziert werden sollen. Das ist notwendig, damit Nginx Anfragen für diese Elemente verwalten kann. In der folgenden Zeile wird Django angewiesen, sie im grundlegenden Projektverzeichnis in einem Verzeichnis mit dem Namen `static` zu platzieren:

~/myprojectdir/myproject/settings.py

```
. . .

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
```

Wenn Sie dies abgeschlossen haben, speichern und schließen Sie die Datei.

### Abschließen der anfänglichen Projekteinrichtung

Jetzt können wir das erste Datenbankschema mit dem Managementskript in unsere PostgreSQL-Datenbank migrieren:

```
~/myprojectdir/manage.py makemigrations
~/myprojectdir/manage.py migrate

```

Erstellen Sie durch folgende Eingabe einen administrativen Benutzer für das Projekt:

```
~/myprojectdir/manage.py createsuperuser

```

Sie müssen einen Benutzernamen auswählen, eine E-Mail-Adresse angeben und ein Passwort bestätigen.

Wir können alle statischen Inhalte am von uns konfigurierten Verzeichnisort sammeln, indem wir Folgendes eingeben:

```
~/myprojectdir/manage.py collectstatic

```

Sie müssen die Operation bestätigen. Die statischen Dateien werden dann in Ihrem Projektverzeichnis in einem Verzeichnis mit dem Namen `static` platziert.

Wenn Sie den Leitfaden zur Ersteinrichtung des Servers befolgt haben, sollte Ihre UFW-Firewall Ihren Server schützen. Um den Entwicklungsserver zu testen, müssen wir Zugriff auf den Port gewähren, den wir dazu verwenden möchten.

Erstellen Sie durch folgende Eingabe eine Ausnahme für Port 8000:

```
sudo ufw allow 8000

```

Schließlich können Sie Ihr Projekt durch Starten des Django-Entwicklungsservers mit diesem Befehl testen:

```
~/myprojectdir/manage.py runserver 0.0.0.0:8000

```

Rufen Sie in Ihrem Webbrowser den Domänennamen oder die IP-Adresse Ihres Servers auf, gefolgt von `:8000`:

```
http://server_domain_or_IP:8000
```

Sie sollten nun die Indexseite von Django erhalten:

![Django-Indexseite](https://assets.digitalocean.com/django_gunicorn_nginx_2004/articles/new_django.index.png)

Wenn Sie am Ende der URL in der Adressleiste `/admin` anfügen, werden Sie zur Eingabe des administrativen Benutzernamens und Passworts aufgefordert, die Sie mit dem Befehl `createsuperuser` erstellt haben:

![Django-Admin-Anmeldung](https://assets.digitalocean.com/articles/django_gunicorn_nginx_1804/admin_login.png)

Nach der Authentifizierung können Sie auf die standardmäßige Admin-Schnittstelle von Django zugreifen:

![Django-Admin-Schnittstelle](https://assets.digitalocean.com/articles/django_gunicorn_nginx_1804/admin_interface.png)

Wenn Sie mit der Erkundung fertig sind, klicken Sie im Terminalfenster auf **Strg+C**, um den Entwicklungsserver herunterzufahren.

### Testen der Fähigkeit von Gunicorn zum Bereitstellen des Projekts

Das Letzte, was wir tun möchten, bevor wir unsere virtuelle Umgebung verlassen, ist Gunicorn zu testen. Dadurch wollen wir sicherstellen, dass die Anwendung bereitgestellt werden kann. Wir geben dazu unser Projektverzeichnis ein und verwenden `gunicorn` zum Laden des WSGI-Moduls des Projekts:

```
cd ~/myprojectdir
gunicorn --bind 0.0.0.0:8000 myproject.wsgi

```

Dadurch wird Gunicorn an der gleichen Schnittstelle gestartet, an der auch der Django-Server ausgeführt wurde. Sie können zurückgehen und die Anwendung erneut testen.

**Anmerkung:** Die Admin-Schnittstelle wird keinen der verwendeten Stile verwenden, da Gunicorn nicht weiß, wo der dafür zuständige statische CSS-Inhalt zu finden ist.

Wir haben Gunicorn einem Modul übergeben, indem wir mithilfe der Modulsyntax von Python den relativen Verzeichnispfad zur Datei `wsgi.py` von Django angegeben haben. Diese ist der Einstiegspunkt für unsere Anwendung. In dieser Datei ist eine Funktion namens `application` definiert, die zur Kommunikation mit der Anwendung dient. Um mehr über die WSGI-Spezifikation zu erfahren, klicken Sie [hier](https://www.digitalocean.com/community/tutorials/how-to-set-up-uwsgi-and-nginx-to-serve-python-apps-on-ubuntu-14-04#definitions-and-concepts).

Wenn Sie mit dem Testen fertig sind, drücken Sie im Terminalfenster auf **Strg+C**, um Gunicorn anzuhalten.

Wir sind nun fertig mit der Konfiguration unserer Django-Anwendung. Wir können unsere virtuelle Umgebung durch folgende Eingabe verlassen:

```
deactivate

```

Der Indikator für die virtuelle Umgebung in Ihrer Eingabeaufforderung wird entfernt.

## Erstellen von systemd-Socket- und Service-Dateien für Gunicorn

Wir haben getestet, ob Gunicorn mit unserer Django-Anwendung interagieren kann. Wir sollten jedoch eine effektivere Methode zum Starten und Anhalten des Anwendungsservers implementieren. Dazu erstellen wir systemd-Service- und Socket-Dateien.

Das Gunicorn-Socket wird beim Booten erstellt und nach Verbindungen lauschen. Wenn eine Verbindung hergestellt wird, startet systemd automatisch den Gunicorn-Prozess, um die Verbindung zu verwalten.

Erstellen und öffnen Sie zunächst eine systemd-Socket-Datei für Gunicorn mit `sudo`-Berechtigungen:

```
sudo nano /etc/systemd/system/gunicorn.socket

```

Darin erstellen wir einen Abschnitt `[Unit]`, um das Socket zu beschreiben, einen Abschnitt `[Socket]`, um den Ort des Sockets zu definieren, und einen Abschnitt `[Install]`, um sicherzustellen, dass das Socket zum richtigen Zeitpunkt erstellt wird:

/etc/systemd/system/gunicorn.socket

```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

Wenn Sie dies abgeschlossen haben, speichern und schließen Sie die Datei.

Erstellen und öffnen Sie in Ihrem Texteditor als Nächstes eine systemd-Service-Datei für Gunicorn mit `sudo`-Berechtigungen. Der Name der Service-Datei sollte mit Ausnahme der Erweiterung mit dem Namen der Socket-Datei übereinstimmen:

```
sudo nano /etc/systemd/system/gunicorn.service

```

Beginnen Sie mit dem Abschnitt `[Unit]`, mit dem Metadaten und Abhängigkeiten angegeben werden. Wir werden hier eine Beschreibung unseres Diensts eingeben und das Init-System anweisen, ihn erst zu starten, nachdem das Netzwerkziel erreicht wurde. Da sich unser Dienst auf das Socket aus der Socket-Datei bezieht, müssen wir eine `Requires`-Direktive einschließen, um diese Beziehung anzugeben:

/etc/systemd/system/gunicorn.service

```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target
```

Als Nächstes werden wir den Abschnitt `[Service]` öffnen. Wir werden den Benutzer und die Gruppe angeben, unter denen wir den Prozess ausführen möchten. Wir wollen unserem regulären Benutzerkonto die Prozessverantwortung übergeben, da es alle relevanten Dateien besitzt. Wir werden der Gruppe `www-data` die Gruppenverantwortung übergeben, damit Nginx einfach mit Gunicorn kommunizieren kann.

Dann werden wir das Arbeitsverzeichnis zuordnen und den Befehl zum Starten des Diensts angeben. In diesem Fall müssen wir den vollständigen Pfad zur ausführbaren Gunicorn-Datei angeben, die in unserer virtuellen Umgebung installiert ist. Wir werden den Prozess mit dem im Verzeichnis `/run` erstellten Unix-Socket verknüpfen, damit der Prozess mit Nginx kommunizieren kann. Wir protokollieren alle Daten in der Standardausgabe, damit der `journald`-Prozess die Gunicorn-Protokolle erfassen kann. Außerdem können wir hier optionale Gunicorn-Optimierungen angeben. Beispielsweise haben wir in diesem Fall drei Workerprozesse angegeben:

/etc/systemd/system/gunicorn.service

```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=sammy
Group=www-data
WorkingDirectory=/home/sammy/myprojectdir
ExecStart=/home/sammy/myprojectdir/myprojectenv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          myproject.wsgi:application
```

Schließlich werden wir einen Abschnitt `[Install]` hinzufügen. Dies teilt systemd mit, womit dieser Dienst verknüpft werden soll, wenn wir festlegen, dass er während des Startvorgangs starten soll. Wir wollen, dass dieser Dienst startet, wenn das normale Mehrbenutzersystem arbeitet.

/etc/systemd/system/gunicorn.service

```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=sammy
Group=www-data
WorkingDirectory=/home/sammy/myprojectdir
ExecStart=/home/sammy/myprojectdir/myprojectenv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          myproject.wsgi:application

[Install]
WantedBy=multi-user.target
```

Damit ist unsere systemd-Dienstdatei fertiggestellt. Speichern und schließen Sie diese jetzt.

Wir können nun starten und das Gunicorn-Socket aktivieren. Dadurch wird die Socket-Datei nun unter `/run/gunicorn.sock` und beim Booten erstellt. Wenn eine Verbindung zu diesem Socket hergestellt wird, startet systemd automatisch den `gunicorn.service`, um die Verbindung zu verwalten:

```
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

```

Wir können uns vergewissern, dass der Vorgang erfolgreich war, indem wir nach der Socket-Datei suchen.

## Suchen nach der Gunicorn-Socket-Datei

Überprüfen Sie den Status des Prozesses, um herauszufinden, ob er gestartet werden konnte:

```
sudo systemctl status gunicorn.socket

```

Sie sollten eine Ausgabe wie diese erhalten:

```
Output● gunicorn.socket - gunicorn socket
     Loaded: loaded (/etc/systemd/system/gunicorn.socket; enabled; vendor prese>
     Active: active (listening) since Fri 2020-06-26 17:53:10 UTC; 14s ago
   Triggers: ● gunicorn.service
     Listen: /run/gunicorn.sock (Stream)
      Tasks: 0 (limit: 1137)
     Memory: 0B
     CGroup: /system.slice/gunicorn.socket
```

Überprüfen Sie als Nächstes, ob die Datei `gunicorn.sock` im Verzeichnis `/run` vorhanden ist:

```
file /run/gunicorn.sock

```

```
Output/run/gunicorn.sock: socket
```

Wenn der Befehl `systemctl status` angegeben hat, dass ein Fehler aufgetreten ist, oder Sie die Datei `gunicorn.sock` im Verzeichnis nicht finden können, ist dies ein Hinweis darauf, dass das Gunicorn-Socket nicht richtig erstellt wurde. Überprüfen Sie die Protokolle des Gunicorn-Sockets durch folgende Eingabe:

```
sudo journalctl -u gunicorn.socket

```

Werfen Sie einen erneuten Blick auf Ihre Datei `/etc/systemd/system/gunicorn.socket`, um alle vorhandenen Probleme zu beheben, bevor Sie fortfahren.

## Testen der Socket-Aktivierung

Wenn Sie derzeit nur die Einheit `gunicorn.socket` gestartet haben, wird der `gunicorn.service` aktuell noch nicht aktiv sein, da das Socket noch keine Verbindungen erhalten hat. Geben Sie zum Überprüfen Folgendes ein:

```
sudo systemctl status gunicorn

```

```
Output● gunicorn.service - gunicorn daemon
   Loaded: loaded (/etc/systemd/system/gunicorn.service; disabled; vendor preset: enabled)
   Active: inactive (dead)
```

Zum Testen des Socket-Aktivierungsverfahrens können wir über `curl` eine Verbindung an das Socket senden, indem wir Folgendes eingeben:

```
curl --unix-socket /run/gunicorn.sock localhost

```

Sie sollten die HTML-Ausgabe von Ihrer Anwendung im Terminal erhalten. Das bedeutet, dass Gunicorn gestartet wurde und Ihre Django-Anwendung bereitstellen konnte. Sie können überprüfen, ob der Gunicorn-Service ausgeführt wird, indem Sie Folgendes eingeben:

```

```

```
Output

● gunicorn.service - gunicorn daemon
     Loaded: loaded (/etc/systemd/system/gunicorn.service; disabled; vendor preset: enabled)
     Active: active (running) since Fri 2020-06-26 18:52:21 UTC; 2s ago
TriggeredBy: ● gunicorn.socket
   Main PID: 22914 (gunicorn)
      Tasks: 4 (limit: 1137)
     Memory: 89.1M
     CGroup: /system.slice/gunicorn.service
             ├─22914 /home/sammy/myprojectdir/myprojectenv/bin/python /home/sammy/myprojectdir/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunico>
             ├─22927 /home/sammy/myprojectdir/myprojectenv/bin/python /home/sammy/myprojectdir/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunico>
             ├─22928 /home/sammy/myprojectdir/myprojectenv/bin/python /home/sammy/myprojectdir/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunico>
             └─22929 /home/sammy/myprojectdir/myprojectenv/bin/python /home/sammy/myprojectdir/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunico>

Jun 26 18:52:21 django-tutorial systemd[1]: Started gunicorn daemon.
Jun 26 18:52:21 django-tutorial gunicorn[22914]: [2020-06-26 18:52:21 +0000] [22914] [INFO] Starting gunicorn 20.0.4
Jun 26 18:52:21 django-tutorial gunicorn[22914]: [2020-06-26 18:52:21 +0000] [22914] [INFO] Listening at: unix:/run/gunicorn.sock (22914)
Jun 26 18:52:21 django-tutorial gunicorn[22914]: [2020-06-26 18:52:21 +0000] [22914] [INFO] Using worker: sync
Jun 26 18:52:21 django-tutorial gunicorn[22927]: [2020-06-26 18:52:21 +0000] [22927] [INFO] Booting worker with pid: 22927
Jun 26 18:52:21 django-tutorial gunicorn[22928]: [2020-06-26 18:52:21 +0000] [22928] [INFO] Booting worker with pid: 22928
Jun 26 18:52:21 django-tutorial gunicorn[22929]: [2020-06-26 18:52:21 +0000] [22929] [INFO] Booting worker with pid: 22929



```

Wenn die Ausgabe von `curl` oder die Ausgabe von `systemctl status` anzeigt, dass ein Problem aufgetreten ist, prüfen Sie die Protokolle auf wei

```

Überprüfen Sie Ihre Datei `/etc/systemd/system/gunicorn.service` auf Probleme. Wenn Sie Änderungen an der Datei `/etc/systemd/system/gunicorn.service` vornehmen, laden Sie das Daemon neu, um die Dienstdefinition neu zu lesen, und starten Sie den Gunicorn-Prozess neu, indem Sie Folgendes eingeben:

```
sudo systemctl daemon-reload
sudo systemctl restart gunicorn

```

Sorgen Sie dafür, dass die oben genannten Probleme behoben werden, bevor Sie fortfahren.

## Konfigurieren von Nginx zur Proxy-Übergabe an Gunicorn

Nachdem Gunicorn eingerichtet ist, müssen wir nun Nginx so konfigurieren, dass Datenverkehr an den Prozess übergeben wird.

Erstellen und öffnen Sie zunächst einen neuen Serverblock im Verzeichnis `sites-available` von Nginx:

```
sudo nano /etc/nginx/sites-available/myproject

```

Öffnen Sie darin einen neuen Serverblock. Wir geben zunächst an, dass dieser Block am normalen Port 80 lauschen und auf den Domänennamen oder die IP-Adresse unseres Servers reagieren soll:

/etc/nginx/sites-available/myproject

```
server {
    listen 80;
    server_name server_domain_or_IP;
}
```

Als Nächstes weisen wir Nginx an, alle Probleme bei der Suche nach einem Favicon zu ignorieren. Außerdem teilen wir Nginx mit, wo die statischen Assets zu finden sind, die wir in unserem Verzeichnis `~/myprojectdir/static` gesammelt haben. Alle diese Dateien verfügen über das Standard-URI-Präfix “/static”; daher können wir einen Ortsblock erstellen, um diese Anfragen abzugleichen:

/etc/nginx/sites-available/myproject

```
server {
    listen 80;
    server_name server_domain_or_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/sammy/myprojectdir;
    }
}
```

Schließlich erstellen wir einen `location / {}`-Block zum Abgleichen aller anderen Anforderungen. In diesen Block werden wir die standardmäßige Datei `proxy_params` einschließen, die in der Nginx-Installation enthalten ist, und dann den Datenverkehr direkt an das Gunicorn-Socket übergeben.

/etc/nginx/sites-available/myproject

```
server {
    listen 80;
    server_name server_domain_or_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/sammy/myprojectdir;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

Wenn Sie dies abgeschlossen haben, speichern und schließen Sie die Datei. Jetzt können wir die Datei aktivieren, indem wir sie mit dem Verzeichnis `sites-enabled` verknüpfen:

```
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled

```

Prüfen Sie Ihre Nginx-Konfiguration durch folgende Eingabe auf Syntaxfehler:

```
sudo nginx -t

```

Wenn keine Fehler gemeldet werden, fahren Sie fort und starten Sie Nginx neu, indem Sie Folgendes eingeben:

```
sudo systemctl restart nginx

```

Schließlich müssen wir unsere Firewall an Port 80 für normalen Datenverkehr öffnen. Da wir keinen Zugriff mehr auf den Entwicklungsserver benötigen, können wir außerdem die Regel zum Öffnen von Port 8000 entfernen:

```
sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'

```

Sie sollten nun in der Lage sein, die Domäne oder IP-Adresse Ihres Servers aufzurufen, um Ihre Anwendung anzuzeigen.

**Anmerkung:** Nach der Konfiguration von Nginx sollte der nächste Schritt aus dem Sichern des Datenverkehrs zum Server mit SSL/TLS bestehen. Das ist äußerst wichtig, da ohne SSL/TLS alle Informationen, einschließlich Passwörter, in Klartext über das Netzwerk gesendet werden.

Wenn Sie einen Domänennamen haben, ist Let’s Encrypt der einfachste Weg, um sich ein SSL-Zertifikat zum Sichern Ihres Datenverkehrs zu verschaffen. Folgen Sie [diesem Leitfaden](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04) zum Einrichten von Let’s Encrypt mit Nginx unter Ubuntu 20.04. Befolgen Sie das Verfahren mit dem Nginx-Serverblock, den wir in diesem Leitfaden erstellt haben.

## Fehlerbehebung bei Nginx und Gunicorn

Wenn Ihre Anwendung in diesem letzten Schritt nicht angezeigt wird, müssen Sie Probleme mit Ihrer Installation beheben.

### Nginx zeigt anstelle der Django-Anwendung die Standardseite an

Wenn Nginx die Standardseite und nicht einen Proxy zu Ihrer Anwendung anzeigt, bedeutet das in der Regel, dass Sie den `server_name` in der Datei `/etc/nginx/sites-available/myproject` so ändern müssen, dass er auf die IP-Adresse oder den Domänennamen Ihres Servers verweist.

Nginx verwendet den `server_name`, um zu bestimmen, welcher Serverblock für Antworten auf Anfragen verwendet werden soll. Wenn Sie die Nginx-Standardseite erhalten, ist das ein Zeichen dafür, dass Nginx die Anfrage nicht explizit mit einem Serverblock abgleichen konnte. Darum greift Nginx auf den Standardblock zurück, der in `/etc/nginx/sites-available/default` definiert ist.

Der `server_name` im Serverblock Ihres Projekts muss spezifischer sein als der im auszuwählenden standardmäßigen Serverblock.

### Nginx zeigt anstelle der Django-Anwendung einen 502-Fehler (Ungültiges Gateway) an

Ein 502-Fehler zeigt, dass Nginx die Anfrage per Proxy nicht erfolgreich vermitteln kann. Eine Vielzahl von Konfigurationsproblemen äußern sich in einem 502-Fehler; für eine angemessene Fehlerbehebung sind also weitere Informationen erforderlich.

Der primäre Ort zur Suche nach weiteren Informationen sind die Fehlerprotokolle von Nginx. Generell werden sie Ihnen mitteilen, welche Bedingungen während des Proxying-Ereignisses Probleme verursacht haben. Folgen Sie den Nginx-Fehlerprotokollen, indem Sie Folgendes eingeben:

```
sudo tail -F /var/log/nginx/error.log

```

Erstellen Sie nun in Ihrem Browser eine weitere Anfrage zur Generierung eines neuen Fehlers (versuchen Sie, die Seite zu aktualisieren). Sie sollten eine neue Fehlermeldung erhalten, die in das Protokoll geschrieben wird. Wenn Sie sich die Nachricht ansehen, sollten Sie das Problem eingrenzen können.

Sie erhalten möglicherweise die folgende Meldung:

**connect() to unix:/run/gunicorn.sock failed (2: No such file or directory)**

Das bedeutet, dass Nginx die Datei `gunicorn.sock` am angegebenen Ort nicht finden konnte. Sie sollten den `proxy_pass`-Ort, der in der Datei `/etc/nginx/sites-available/myproject` definiert ist, mit dem tatsächlichen Ort der Datei `gunicorn.sock` vergleichen, die von der Datei `gunicorn.socket` generiert wurde.

Wenn Sie keine `gunicorn.sock`-Datei im Verzeichnis `/run` finden können, bedeutet das im Allgemeinen, dass die systemd-Socket-Datei sie nicht erstellen konnte. Kehren Sie zurück zum [Abschnitt zum Suchen nach der Gunicorn-Socket-Datei](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-20-04-de#checking-for-the-gunicorn-socket-file), um die Schritte zur Fehlerbehebung für Gunicorn zu durchlaufen.

**connect() to unix:/run/gunicorn.sock failed (13: Permission denied)**

Das bedeutet, dass Nginx aufgrund von Berechtigungsproblemen keine Verbindung zum Gunicorn-Socket herstellen konnte. Dies kann geschehen, wenn das Verfahren mit dem root user anstelle eines `sudo`-Benutzers ausgeführt wird. Zwar kann systemd die Gunicorn-Socket-Datei erstellen, doch kann Nginx nicht darauf zugreifen.

Dies kann geschehen, wenn es an einem beliebigen Punkt zwischen dem root-Verzeichnis (`/`) der Datei `gunicorn.sock` begrenzte Berechtigungen gibt. Wir können die Berechtigungen und Verantwortungswerte der Socket-Datei und jedes der übergeordneten Verzeichnisse überprüfen, indem wir den absoluten Pfad zu unserer Socket-Datei dem Befehl `namei` übergeben:

```
namei -l /run/gunicorn.sock

```

```
Outputf: /run/gunicorn.sock
drwxr-xr-x root root /
drwxr-xr-x root root run
srw-rw-rw- root root gunicorn.sock
```

Die Ausgabe zeigt die Berechtigungen der einzelnen Verzeichniskomponenten an. Indem wir uns die Berechtigungen (erste Spalte), den Besitzer (zweite Spalte) und den Gruppenbesitzer (dritte Spalte) ansehen, können wir ermitteln, welche Art des Zugriffs auf die Socket-Datei erlaubt ist.

Im obigen Beispiel haben die Socket-Datei und die einzelnen Verzeichnisse, die zur Socket-Datei führen, globale Lese- und Ausführungsberechtigungen (die Berechtigungsspalte für die Verzeichnisse endet mit `r-x` anstelle von `---`). Der Nginx-Prozess sollte erfolgreich auf das Socket zugreifen können.

Wenn eines der Verzeichnisse, das zum Socket führt, keine globale Lese- und Ausführungsberechtigung aufweist, kann Nginx nicht auf das Socket zugreifen, ohne globale Lese- und Ausführungsberechtigungen zuzulassen oder sicherzustellen, dass die Gruppenverantwortung einer Gruppe erteilt wird, zu der Nginx gehört.

### Django zeigt an: “could not connect to server: Connection refused”

Eine Meldung, die Sie bei dem Versuch, im Webbrowser auf Teile der Anwendung zuzugreifen, von Django erhalten können, lautet:

```
OperationalError at /admin/login/
could not connect to server: Connection refused
    Is the server running on host "localhost" (127.0.0.1) and accepting
    TCP/IP connections on port 5432?
```

Das bedeutet, dass Django keine Verbindung zur Postgres-Datenbank herstellen kann. Vergewissern Sie sich durch folgende Eingabe, dass die Postgres-Instanz ausgeführt wird:

```
sudo systemctl status postgresql

```

Wenn nicht, können Sie sie starten und so aktivieren, dass sie beim Booten automatisch gestartet wird (wenn sie nicht bereits entsprechend konfiguriert ist); geben Sie dazu Folgendes ein:

```
sudo systemctl start postgresql
sudo systemctl enable postgresql

```

Wenn Sie weiter Probleme haben, stellen Sie sicher, dass die in der Datei `~/myprojectdir/myproject/settings.py` definierten Datenbankeinstellungen korrekt sind.

### Weitere Fehlerbehebung

Bei der weiteren Fehlerbehebung können die Protokolle dazu beitragen, mögliche Ursachen einzugrenzen. Prüfen Sie sie nacheinander und suchen Sie nach Meldungen, die auf Problembereiche hinweisen.

Folgende Protokolle können hilfreich sein:

-   Prüfen Sie die Nginx-Prozessprotokolle, indem Sie Folgendes eingeben: `sudo journalctl -u nginx`
-   Prüfen Sie die Nginx-Zugangsprotokolle, indem Sie Folgendes eingeben: `sudo less /var/log/nginx/access.log`
-   Prüfen Sie die Nginx-Fehlerprotokolle, indem Sie Folgendes eingeben: `sudo less /var/log/nginx/error.log`
-   Prüfen Sie die Gunicorn-Anwendungsprotokolle, indem Sie Folgendes eingeben: `sudo journalctl -u gunicorn`
-   Prüfen Sie die Gunicorn-Socket-Protokolle, indem Sie Folgendes eingeben: `sudo journalctl -u gunicorn.socket`

Wenn Sie Ihre Konfiguration oder Anwendung aktualisieren, müssen Sie die Prozesse wahrscheinlich neu starten, damit Ihre Änderungen aktiv werden.

Wenn Sie Ihre Django-Anwendung aktualisieren, können Sie den Gunicorn-Prozess durch folgende Eingabe neu starten, um die Änderungen zu erfassen:

```
sudo systemctl restart gunicorn

```

Wenn Sie Gunicorn-Socket- oder Service-Dateien ändern, laden Sie das Daemon neu und starten Sie den Prozess neu, indem Sie Folgendes eingeben:

```
sudo systemctl daemon-reload
sudo systemctl restart gunicorn.socket gunicorn.service

```

Wenn Sie die Konfiguration des Nginx-Serverblocks ändern, testen Sie die Konfiguration und dann Nginx, indem Sie Folgendes eingeben:

```
sudo nginx -t && sudo systemctl restart nginx

```

Diese Befehle sind hilfreich, um Änderungen zu erfassen, während Sie Ihre Konfiguration anpassen.

## Zusammenfassung

In diesem Leitfaden haben wir ein Django-Projekt in seiner eigenen virtuellen Umgebung eingerichtet. Wir haben Gunicorn so konfiguriert, dass Clientanfragen übersetzt werden, damit Django sie verwalten kann. Anschließend haben wir Nginx als Reverseproxy eingerichtet, um Clientverbindungen zu verwalten und je nach Clientanfrage das richtige Projekt bereitzustellen.

Django macht die Erstellung von Projekten und Anwendungen durch Bereitstellung vieler der gängigen Elemente besonders einfach; so können Sie sich ganz auf die individuellen Elemente konzentrieren. Durch Nutzung der in diesem Artikel beschriebenen allgemeinen Tool Chain können Sie die erstellten Anwendungen bequem über einen einzelnen Server bereitstellen.

---