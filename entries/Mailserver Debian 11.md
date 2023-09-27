Hier ist sie - die von einigen Lesern sehnsüchtig erwartete Aktualisierung meiner Mailserver-Anleitung für Debian Buster. Große Teile der [Vorgängerversion für Debian Stretch](https://thomas-leister.de/mailserver-debian-stretch/) habe ich übernommen. Gleichzeitig sind Detailverbesserungen in das Setup eingeflossen. Ein vollständiges [Changelog](https://thomas-leister.de/mailserver-debian-buster/#%C3%A4nderungen-zur-vorg%C3%A4ngerversion-mailserver-unter-debian-stretch) findet sich am Ende dieses Beitrags.

Wie auch in den letzten Versionen ist mir wichtig, die Funktionsweise und das Zusammenspiel der Mailserver-Komponenten so zu erklären, dass das Mailsystem als solches in den Grundzügen verstanden werden kann. Ich setze dabei grundlegende Kenntnisse im Bereich Linux-Server voraus; trotzdem ist dieser Guide auch für Anfänger geeignet, die Interesse und Zeit mitbringen.

Wer lieber auf eine fertige Lösung setzt und sich die Handarbeit sparen will, sollte sich einmal [Mailcow](https://mailcow.email/) von André Peters ansehen.

Ein Leser dieser Anleitung hat ein Ansible-Script erstellt, welches das Setup des Mailservers automatisch durchführt: [https://github.com/mubn/ansible-mail-server](https://github.com/mubn/ansible-mail-server)

## Mailserver-Funktionen

Damit ihr einen Eindruck vom Funktionsumfang des fertigen Mailsetups bekommt, hier einige Merkmale:

-   Senden und Empfangen von E-Mails für beliebige Domains
-   Flexible Einrichtung von Domains, Mailaccounts, Aliasen, Weiterleitungen und Regeln für die Transportverschlüsselung über ein MySQL-Backend zur Laufzeit
-   Nutzer-spezifisch begrenztes Mailbox-Volumen
-   Einrichtung allgemeiner und Nutzer-spezifischer Sieve-Filterregeln zum Filtern und/oder Umsortieren eingehender E-Mails
-   Zuverlässige und moderne Spamerkennung via Rspamd (+ Weboberfläche für Spam-Statistiken)
-   “Send only” Accounts z.B. für NextCloud / Forensoftware / …
-   DKIM-und ARC-Signierung ausgehender E-Mails
-   Mailclient Autokonfiguration
-   Domain Catch-All

Eine **Weboberfläche** / ein **Management-Tool** zur Verwaltung dieses Setups biete ich selbst nach wie vor nicht an. In der Zwischenzeit haben aber andere User Lösungen veröffentlicht, z.B.

-   Florian Kapfenberger: [Mailman](https://github.com/phiilu/mailman) _(nicht zu verwechseln mit Mailman, dem Mailinglist-Manager!)_
-   Andreas Bresch: [VmailManage](https://github.com/Andreas-Bresch/vmailManage/)

-   Henrik Halbritter: [MailAdmin](https://github.com/Halbritter/MailAdmin/releases)
-   awidegreen: [vmail-rs](https://github.com/awidegreen/vmail-rs) (CLI-Tool!)
-   pprugger: [vmail-admin](https://github.com/pprugger/vmail-admin)
-   Kekskurse: [Go-Mail-Admin](https://github.com/kekskurse/go-mail-admin)

Das Datenbank-Layout und die Struktur des `/var/vmail`-Verzeichnisses haben sich im Vergleich zur vorherigen Anleitung _nicht_ geändert. Ein Update älterer Setups ist also einfach realisierbar.

---

## Verwendete Software

-   Debian 10 “Buster”
-   Postfix
-   Dovecot
-   Rspamd
-   Redis
-   MariaDB
-   Nginx

## Gegebenheiten

In dieser Anleitung kommen folgende Domains vor:

-   `mysystems.tld`: Übergeordnete, primäre Domain
-   `mail.mysystems.tld`: Subdomain, unter der der Mailserver verfügbar sein soll (FQDN des Mailsystems)
-   `imap.mysystems.tld`: Alias auf mail.mysystems.tld, wird von vielen Mailclient automatisch gesucht und gefunden
-   `smtp.mysystems.tld`: Dasselbe für den SMTP-Dienst
-   `domain2.tld`: Eine zweite Domain neben mysystems.tld, für die E-Mails gesendet und empfangen werden sollen
-   `domain3.tld`: Eine dritte Domain, für die E-Mails gesendet und empfangen werden sollen

**Diese Domains müssen in der _gesamten_ Anleitung selbstverständlich durch eigene ersetzt werden!**  
Auf domain2.tld und domain3.tld kann verzichtet werden, wenn der Mailserver nur für eine Domain (nur für “@mysystems.tld”-Adressen) genutzt werden soll.

Folgende IP-Adressen werden beispielhaft in Konfigurationen genannt und müssen ebenfalls durch die IP-Adressen des jeweiligen Servers ersetzt werden:

-   `2001:db8::1` (IPv6-Adresse des Mailservers)
-   `203.0.113.1` (IPv4-Adresse des Mailservers)

## Grundvoraussetzungen für den Mailserver

-   Ein virtueller oder dedizierter Server mit bereits installiertem Debian 10 Buster  
    (“Standard-Systemwerkzeuge” und “SSH” bei der Installation angewählt)
-   Mindestens eine eigene Domain + volle Kontrolle über die DNS-Zone

Ein kleiner, virtueller Server auf KVM-Basis ist in den meisten Fällen völlig ausreichend. Ich empfehle für kleine, private Setups zwei CPU-Kerne und 1-2 GB RAM. Virtuelle Server kann man z.B. bei [Servercow](https://servercow.de/vserver) oder [Hetzner](https://hetzner.cloud/?ref=H6gtsnaMZj6N) preisgünstig bekommen.

## Komponenten eines vollständigen Mailsystems

![Mailserver Schema](https://thomas-leister.de/mailserver-debian-buster/images/mailserver-schema.png)

Mailserver Schema

Welche Softwarekomponenten verwendet werden, wisst ihr bereits. Doch welche Software übernimmt welche Aufgaben?

### Dovecot

Dovecot ist ein weit verbreiteter MDA (Mail Delivery Agent) und IMAP-Server. Er sortiert ankommende E-Mails in die Postfächer des jeweiligen Empfängers ein und stellt eine Schnittstelle zum Abrufen der Mailbox bereit (IMAP). Außerdem wird Dovecot in diesem Setup von Postfix als sog. SASL-Authentifizierungsserver genutzt: Postfix fragt Dovecot, ob ein bestimmter Benutzer berechtigt ist, sich am System anzumelden.

### Postfix

Postfix wird oft zusammen mit Dovecot eingesetzt. Der populäre MTA (Mail Transfer Agent) kümmert sich um alles, was mit dem Transport der E-Mail zu tun hat: Vom E-Mail Client zum eigenen Mailserver, und von dort aus zum jeweiligen Zielserver. Außerdem nimmt Postfix E-Mails von fremden Servern an und leitet sie an den MDA Dovecot weiter. Antispam-Software wird i.d.R. direkt in Postfix integriert, um eintreffende Spammails erst gar nicht in die Mailbox des Nutzers gelangen zu lassen.

_Anmerkung: Postfix ist “der eigentliche Mailserver”. E-Mails können ohne weiteres einzig und allein mit Postfix gesendet und empfangen werden. Alle weiteren Komponenten wie Dovecot und Rspamd machen uns das Leben allerdings einfacher ;-)_

### MariaDB (MySQL-Datenbank)

Dovecot und Postfix werden so konfiguriert, dass sie eine MySQL-Datenbank als Backend (Datenbasis) nutzen. In der Datenbank werden zu nutzende Domains, Benutzer, Aliase und weitere Daten gespeichert. Durch einfaches Hinzufügen oder Entfernen von Datensätzen in oder aus Datenbanktabellen können neue Benutzer oder Aliase angelegt oder gelöscht werden. Der Vorteil eines Datenbank-Backends ist, dass sich der Mailserver damit sehr einfach verwalten lässt: So ließe sich zur Benutzerverwaltung beispielsweise eine Weboberfläche in PHP entwickeln, die die MySQL-Datenbank verändert. Die Serverkonfiguration muss dann nicht manuell geändert werden.

### Rspamd

Rspamd ist ein Filtersystem, das in Postfix integriert wird und eingehende E-Mails überprüft. Spammails werden von Rspamd erkannt und nicht an den Benutzer zugestellt bzw. aussortiert. Außerdem fügt Rspamd bei ausgehenden E-Mails eine DKIM-Signatur hinzu, sodass fremde Mailserver eigene Mails nicht als verdächtig einstufen.

### Nginx

Nginx ist ein weit verbreiteter und schlanker Webserver / Webproxy. In diesem Setup hat er mehrere Aufgaben: Zum einen kann er als Endpunkt für den Ausstellungsprozess von Let’s Encrypt-Zertifikaten dienen, zum anderen als Proxy für die Rspamd-Weboberfläche, oder um die Autokonfigurationsdatei für Mailclients anzubieten.

### Redis

Redis ist ein hochperformanter In-memory Key-Value-Store, also eine sehr einfache, schnelle Datenbank, welche Schlüssel-Wert-Paare effizient im Speicher ablegen kann. Rspamd nutzt Redis, um einige Daten zwischenzuspeichern (wie z.B. zuletzt überprüfte Mailserver).

## Vorbereitungen

### Tipp: Reinen Tisch machen

Wenn ihr den Server vorher schon für etwas anderes (oder sogar ein anderes Mail-Setup) verwendet habt, stellt sicher, dass Reste aus alten Installationen das neue Setup nicht behindern. Speziell vorherige Mailserver-Versuche sollten rückstandslos entfernt werden (inkl. der zugehörigen Konfigurationsdateien). Am besten ist natürlich – falls möglich – eine komplette Neuinstallation des Servers. Ich empfehle, den Mailserver als eigenständiges System zu betreiben und auf demselben Host keine anderen Dienste zu installieren, um die Integrität des Mailsystems sicherzustellen.

Im Folgenden gehe ich von einem frisch installierten Debian 10 Buster aus (zusätzlich nur “Standard-Systemwerkzeuge” und SSH installiert).

### Login als Root

Bei der Installation von Debian wird ein normaler Benutzeraccount, z.B. “thomas” eingerichtet, zu dem ihr euch via Passwort verbinden könnt. Der Root-Account ist standardmäßig nicht direkt zugänglich, sondern nur über den Umweg via “su”. Für diese Anleitung werden permanent Root-Rechte benötigt. Öffnet nach dem Login am Server also am besten eine Root-Kommandozeile via

```
su -
```

Gebt dann das Passwort für euren root-User ein.

### System aktualisieren

Bevor ihr neue Software-Pakete installiert, solltet ihr mittels

```
apt update && apt upgrade
```

sicherstellen, dass euer System aktuell ist. Bei der Gelegenheit bietet sich auch gleich ein Reboot an, um einen möglicherweise aktualisierten Linux-Kernel zu laden.

### Hostname und Server-FQDN setzen

Euer Server bekommt zwei Namen, über die er identifiziert werden kann:

-   Lokalen Hostnamen: Für die Identifizierung des Servers innerhalb der eigenen Infrastruktur, z.B. “mail”
-   FQDN (Fully Qualified Domain Name): Für die weltweite Identifizierung im Internet, z.B. “mail.mysystems.tld”

Der FQDN muss nicht zwingend etwas mit den Domains zu tun haben, für die später E-Mails gesendet und empfangen werden sollen. Wichtig ist nur, dass euer künftiger Mailserver einen solchen Namen hat, der auch über das DNS zur Server-IP-Adresse aufgelöst werden kann (dazu gleich mehr im Abschnitt “Einrichtung des DNS”). Den lokalen Hostnamen setzt ihr wie folgt:

```
hostnamectl set-hostname --static mail
```

In der Hosts-Datei `/etc/hosts` sollten FQDN und lokaler Hostname hinterlegt sein. Die Datei kann beispielsweise so aussehen:

```
127.0.0.1	localhost
127.0.1.1	mail.mysystems.tld	mail

::1         localhost ip6-localhost ip6-loopback
ff02::1     ip6-allnodes
ff02::2     ip6-allrouters
```

Die Ausgaben der Kommandos `hostname` und `hostname --fqdn` sollten nach den Änderungen wie folgt aussehen:

```
root@mail:~# hostname
mail
root@mail:~# hostname --fqdn
mail.mysystems.tld
```

Der FQDN (in diesem Beispiel “mail.mysystems.tld”) wird außerdem nach `/etc/mailname` geschrieben:

```
echo $(hostname -f) > /etc/mailname
```

_(Der Hostname im Shell-Prompt z.B. `root@meinhost:` passt sich erst nach einem erneuten Login an.)_

### Unbound DNS Resolver installieren

Das Mailsystem benötigt einen funktionierenden DNS-Server (Resolver), sodass die Herkunft von E-Mails überprüft werden kann. Auch der Rspamd-Spamfilter verlässt sich bei der Bewertung von Spammails auf DNS-Dienste. Eine schnelle Namesauflösung bringt also Performancevorteile für das ganze Mailsystem. Für den Zugriff auf Spamhaus-Blocklists kann es sogar notwendig sein, seinen eigenen DNS-Resolver zu nutzen, weil z.B. Zugriffe über das Google DNS blockiert werden. Deshalb (und um die Sicherheit im Bezug auf Abhängigkeiten zu fremden Systemen zu verbessern) empfehle ich die Nutzung eines eigenen, lokalen DNS-Resolvers.

Unbound installieren:

```
apt install unbound
```

Für die nächsten Kommandos muss müssen die Pakete `dnsutils` und `resolvconf` installiert sein. Wenn bei der Installation von Debian die “Standard-Systemwerkzeuge” ausgewählt wurden, sind die `dnsutils` schon installiert.

Ein `dig @::1 denic.de +short +dnssec` sollte eine ähnliche Ausgabe wie folgt erzeugen:

```
# dig @::1 denic.de +short +dnssec
A 8 2 3600 20170814090000 20170731090000 26155 denic.de. Jo90qnkLkZ6gI4qNHj19BMguFuGof9hCPhdeSh/fSePSQ/WXlWMmfjW1 sNDJ/bcITRMyz8DQdDzmWPDIeSJ/qPyfoZ+BjUZxtaXcs0BAl4KX8q7h R05TGmAbgPhrYBoUKJkU/q8T+jWKHAJRUeWbCd8QOJsJbneGcUKxRAPe i6Rq51/OL/id6zUCtalhclah2TfLLaqku9PmKwjbGdZm11BXSr8b56LB WX/rdLIrKWNpE+jHGAUMmDsZL84Kx3Oo
```

Wenn der `dig`-Befehl funktioniert hat, kann der lokale Resolver als primärer Resolver gesetzt werden:

```
apt install resolvconf
echo "nameserver ::1" >> /etc/resolvconf/resolv.conf.d/head
```

ein `nslookup denic.de | grep Server` sollte nun

```
Server:		::1
```

zurückliefern. Damit ist der lokale DNS-Resolver als Haupt-Resolver einsatzbereit.

## Einrichtung des DNS

Zu Beginn dieser Anleitung wurde für den Mailserver der FQDN “mail.mysystems.tld” festgelegt. Für diesen Domain-Namen werden nun A-Records im DNS-Zonefile der Domain “mysystems.tld” erstellt. Loggt euch bei eurem Domain-Provider ein und legt die folgenden Einträge an – der erste für die IPv4-IP-Adresse des Mailservers, die zweite für die IPv6-Adresse. (Beispiel!):

Achtet im Folgenden vor allem auf den abschließenden Punkt in den Domainnamen!

```
mail.mysystems.tld. 86400 IN A    203.0.113.1
mail.mysystems.tld. 86400 IN AAAA 2001:db8::1
```

“mail.mysystems.tld” ist damit im DNS bekannt. Wenn keine IPv6-Adresse genutzt wird, kann der zweite Record entfallen. Bleiben noch “imap.mysystems.tld” und “smtp.mysystems.tld”, die als Alias-Domains für “mail.mysystems.tld” angelegt werden. Sie sind nicht unbedingt notwendig, werden von vielen Mailclient aber gesucht und sind so üblich:

```
imap.mysystems.tld. 86400 IN CNAME mail.mysystems.tld.
smtp.mysystems.tld. 86400 IN CNAME mail.mysystems.tld.
```

Mailclients können sich damit schon über imap.mysystems.tld und smtp.mysystems.tld zum Mailserver verbinden. Andere Mailserver suchen bei der E-Mail-Übermittlung allerdings nicht nach A- oder CNAME-Records, sondern nach MX-Records. Ein MX-Record zeigt, welcher Mailserver für die E-Mails zu einer Domain zuständig ist. In meinem Beispiel soll sich unser Mailserver neben den E-Mails für mysystems.tld auch um die Mails für domain2.tld und domain3.tld kümmern.

Im Zonefile der Domain “mysystems.tld” wird dazu dieser Record angelegt:

```
mysystems.tld. 86400 IN MX 0 mail.mysystems.tld.
```

In die Zonefiles der anderen Domains werden entsprechend die Records

```
domain2.tld. 86400 IN MX 0 mail.mysystems.tld.
```

und

```
domain3.tld. 86400 IN MX 0 mail.mysystems.tld.
```

angelegt.

### Reverse DNS

Des weiteren muss ein sog. Reverse-DNS-Record / PTR für den FQDN des Mailservers angelegt werden. Dieser entspricht der Umkehrung eines normalen DNS-Records und ordnet einer IP-Adresse einen Hostnamen zu. Diesen Record kann nur der Inhaber des Netzes anlegen, aus dem eure IP-Adresse stammt. Möglicherweise könnt ihr so einen Reverse-DNS-Record in der Verwaltungsoberfläche eures Serveranbieters setzen, oder ihr bittet den Support, das zu tun. Der Domain-Name, der mit der IP-Adresse verknüpft werden muss, ist der FQDN eures Mailservers. In meinem Beispiel mail.mysystems.tld. Denkt daran, für alle vom Mailserver genutzten, öffentlichen IP-Adressen einen solchen Record zu erstellen. In dieser Anleitung wird eine IPv4- und eine IPv6-Adresse verwendet.

### SPF-Records

Im Kampf gegen Spam und Phishing wurde das sog. Sender Policy Framework entwickelt (Siehe auch Beitrag: “[Voraussetzungen für den Versand zu großen E-Mail Providern](https://thomas-leister.de/voraussetzungen-email-versand-gro%C3%9Fe-provider/)"). Obwohl es sich nur als eingeschränkt brauchbar erwiesen hat, erwarten die meisten Mailprovider gültige SPF-Records für andere Mailserver und prüfen diese. SPF-Einträge werden im Zonefile aller Domains erstellt, für die ein Mailserver E-Mails verschickt, und geben an, welche Server für eine Domain sendeberechtigt sind. Für unsere Domain mysystems.tld wird der folgende Record im Zonefile von mysystems.tld angelegt:

```
mysystems.tld. 3600 IN TXT v=spf1 a:mail.mysystems.tld mx ?all
```

Hiermit erhält nur der im A-Record “mail.msystems.tld” genannte Server für mysystems.tld eine Sendeberechtigung. Die Neutral-Einstellung “?all” sorgt dafür, dass E-Mails von anderen Servern trotzdem angenommen werden sollen. Damit gehen wir Problemen beim Mail-Forwarding aus dem Weg. Wir erstellen den SPF-Record also eigentlich nur, damit andere Mailserver unseren Server wegen des existierenden Records positiv bewerten – nicht, weil er seinen Nutzen entfalten soll.

In den Zonefiles der beiden Domains “domain2.tld” und “domain3.tld” wird (angepasst auf die Domain) jeweils dieser Record angelegt:

```
domain2.tld. 3600 IN TXT v=spf1 include:mysystems.tld ?all
```

Über das “include” wird der erste Record der Domain mysystems.tld eingebunden.

### DMARC Records

DMARC-Einträge bestimmen, was ein fremder Mailserver tun soll, wenn eine von ihm empfangene Mail nach SPF- und DKIM-Checks offenbar nicht vom korrekten Mailserver stammt (wenn der Absender also gefälscht wurde). Es ist vernünftig, andere Mailserver anzuweisen, solche E-Mails nicht zu akzeptieren:

```
_dmarc.mysystems.tld.   3600    IN TXT    v=DMARC1; p=reject;
```

Der Record wird entsprechend auch für die anderen Domains gesetzt:

```
_dmarc.domain2.tld.   3600    IN TXT    v=DMARC1; p=reject;
```

Einen DMARC-Record mit einer abweichenden Policy könnt ihr euch unter [https://elasticemail.com/dmarc/](https://elasticemail.com/dmarc/) selbst generieren lassen.

## Erstkonfiguration Nginx Webserver

Wie bereits angemerkt, übernimmt Nginx in diesem Setup verschiedene Aufgaben. Für’s erste dient er aber nur als HTTP-Endpunkt, um Let’s Encrypt Zertifikate zu beantragen. Das ist zwar prinzipiell auch ohne Nginx im standalone-Modus möglich, macht uns aber das Leben einfacher, wenn wir ihn sowieso in Betrieb haben _(=> belegte Ports durch Nginx, ACME client …)_.

Dazu wird Nginx installiert …

```
apt install nginx
```

… und unter `/etc/nginx/sites-available/mail.mysystems.tld` eine neue Konfiguration mit diesem Inhalt angelegt:

```
server {
        listen 80;
        listen [::]:80;
#       listen 443 ssl http2;
#       listen [::]:443 ssl http2;

        server_name mail.mysystems.tld imap.mysystems.tld smtp.mysystems.tld;

#       ssl_certificate /etc/acme.sh/mail.mysystems.tld/fullchain.pem;
#       ssl_certificate_key /etc/acme.sh/mail.mysystems.tld/privkey.pem;

#       add_header Strict-Transport-Security max-age=15768000;

#       if ($ssl_protocol = "") {
#           return 301 https://$server_name$request_uri;
#       }
}
```

Einige Zeilen sind zu diesem Zeitpunkt bewusst auskommentiert und werden später wieder aktiviert, sobald TLS-Zertifikate verfügbar sind.

Der neue vHost kann nun aktiviert werden:

```
ln -s /etc/nginx/sites-available/mail.mysystems.tld /etc/nginx/sites-enabled/mail.mysystems.tld
systemctl reload nginx
```

## Beantragung der TLS-Zertifikate (via Let’s Encrypt)

Gültige TLS-Zertifikate von anerkannten Zertifizierungsstellen (CAs) sind heute für jeden Mailserver ein “muss”. Immer mehr Mailsysteme verweigern zurecht den Empfang über ungesicherte Verbindungen. Was früher (vor allem für den privaten Einsatz) noch ein bedeutender Kostenfaktor war, bekommt man heute Dank Let’s Encrypt kostenlos und sehr unkompliziert. Im folgenden beziehe ich mich daher auf die Generierung von Let’s Encrypt-Zertifikaten. Selbstverständlich können stattdessen auch Zertifikate anderer CAs genutzt werden.

Für Postfix und Dovecot benötigen wir Zertifikate zu folgenden Domains:

-   mail.mysystems.tld
-   imap.mysystems.tld
-   smtp.mysystems.tld

Um die Zertifikate von der Let’s Encrypt Zertifizierungsstelle abholen, nutze ich das schlanke [acme.sh Script](https://github.com/acmesh-official/acme.sh). Dieses verfügt über einen “Nginx-Mode”, in dem das Script den Nginx Webserver automatisch so konfiguriert, dass die Domains von LE verifiziert werden können.

acme.sh installieren:

```
curl https://get.acme.sh | sh
```

Der Hinweis, welcher besagt, dass socat installiert werden solle, kann ignoriert werden. Socat wird in unserem Fall nicht benötigt.

Nach der Installation muss das Shell-Profil neu geladen werden, damit das “acme.sh” Kommando verfügbar gemacht wird:

```
source ~/.profile
```

Zertifikate beantragen und herunterladen:

```
acme.sh --issue --server letsencrypt --nginx \
    -d mail.mysystems.tld \
    -d imap.mysystems.tld \
    -d smtp.mysystems.tld
```

Zertifikate installieren:

```
mkdir -p /etc/acme.sh/mail.mysystems.tld
acme.sh --install-cert -d mail.mysystems.tld \
    --key-file       /etc/acme.sh/mail.mysystems.tld/privkey.pem  \
    --fullchain-file /etc/acme.sh/mail.mysystems.tld/fullchain.pem \
    --reloadcmd     "systemctl reload nginx; systemctl restart dovecot; systemctl restart postfix;"
```

Infolge unseres Reload-Commands wird Acme.sh versuchen, Dovecot und Postfix neu zu laden. Da beide Softwarepakete noch nicht installiert sind, werden euch Fehler angezeigt. Ihr könnt diese zum gegenwärtigen Zeitpunkt aber ignorieren.

Die vorher im Nginx auskommentierten Zeilen in `/etc/nginx/sites-available/mail.mysystems.tld` können durch entfernen der Hashzeichen nun aktiviert und Nginx mittels

```
nginx -t
systemctl reload nginx
```

getestet und neu gestartet werden.

Für die Autokonfiguration der Mailclients wird später noch ein Zertifikat für eine weitere Domain beantragt - doch das kann erst einmal warten.

Damit die automatische Zertifikatserneuerung funktioniert, wird noch der Cronjob für acme.sh aktiviert:

```
 acme.sh --install-cronjob
```

## MySQL Datenbank einrichten

Informationen über zu verwaltende Domains, Benutzer, Weiterleitungen und sonstige Einstellungen soll der Mailserver aus einer MySQL-Datenbank ziehen. Das hat den Vorteil, dass der Server im laufenden Betrieb flexibel angepasst werden kann, ohne die Konfigurationsdateien ändern zu müssen. Die Datenbank ermöglicht uns außerdem ein virtualisiertes Mailserver-Setup: Die Benutzer auf den Mailservern müssen nicht mehr als reale Linux-Benutzer im System registriert sein, sondern nur noch in der Datenbank eingetragen werden.

Als DBMS wird die neue Debian-Standard-MySQL-Datenbank “MariaDB” installiert:

```
apt install mariadb-server
```

Nach der Installation sollte MariaDB bereits gestartet sein. Den Status könnt ihr mittels `systemctl status mysql` (nicht “mariadb!") überprüfen. Falls das nicht der Fall ist, startet den Datenbankserver: `systemctl start mysql`.

Standardmäßig kann sich nur der root-Systemuser am Datenbankserver anmelden. Authentifiziert wird er dabei automatisch via PAM, sodass keine zusätzliche Passworteingabe notwendig ist. Die einfache Eingabe von

```
mysql
```

bringt euch in eine MySQL Root Shell. Über diese werden nun ein paar SQL-Befehle ausgeführt.

Ein SQL-Kommando endet immer mit einem Semikolon `;`. Mehrzeilige Befehle könnt ihr ohne weiteres einfach mit ENTER umbrechen, so wie sie im Folgenden dargestellt werden. Achtet auf den Unterschied zwischen “Tick” (`'`) und “Backtick” ( `\` `) – der Backtick wird mit Shift + 2x Accent-Taste erzeugt. Kopiert die SQL-Statements am besten direkt in eure Zwischenanlage, statt sie mühsam abzutippen.

Im ersten Schritt wird eine neue Datenbank “vmail” angelegt.

```
create database vmail
    CHARACTER SET 'utf8';
```

Ein neuer DB-User `vmail` mit dem Passwort `vmaildbpass` bekommt Zugriff auf diese neue Datenbank _(Wählt ein eigenes Passwort statt “vmaildbpass”!)_:

Nutzt für `vmaildbpass` nur die Zeichen 0-9 a-z und A-z. Einigen Berichten nach können Sonderzeichen zu Problemen führen.

```
grant select on vmail.* to 'vmail'@'localhost' identified by 'vmaildbpass';
```

Alle weiteren Kommandos zu Erstellung der Datenbank-Tabellen sollen sich auf die eben erzeugte Datenbank beziehen:

```
use vmail;
```

Das Mail-Setup soll 4 verschiedene Tabellen nutzen. Kopiert die SQL-Statements einzeln und nacheinander in die MySQL-Kommandozeile und bestätigt jedes mal mit [Enter]. Anpassungen sind nicht notwendig.

### Domain-Tabelle

Die Domain-Tabelle enthält alle Domains, die mit dem Mailserver genutzt werden sollen.

```
CREATE TABLE `domains` (
    `id` int unsigned NOT NULL AUTO_INCREMENT,
    `domain` varchar(255) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY (`domain`)
);
```

### Account-Tabelle

```
CREATE TABLE `accounts` (
    `id` int unsigned NOT NULL AUTO_INCREMENT,
    `username` varchar(64) NOT NULL,
    `domain` varchar(255) NOT NULL,
    `password` varchar(255) NOT NULL,
    `quota` int unsigned DEFAULT '0',
    `enabled` boolean DEFAULT '0',
    `sendonly` boolean DEFAULT '0',
    PRIMARY KEY (id),
    UNIQUE KEY (`username`, `domain`),
    FOREIGN KEY (`domain`) REFERENCES `domains` (`domain`)
);
```

Die Account-Tabelle enthält alle Mailserver-Accounts. Das Feld “quota” enthält die Volumenbegrenzung für die Mailbox in MB (Megabyte). Im Feld “enabled” wird über einen bool’schen Wert festgelegt, ob ein Account aktiv ist, oder nicht. So können einzelne User temporär deaktiviert werden, ohne gelöscht werden zu müssen. “sendonly” wird auf “true” gesetzt, wenn der Account nur zum Senden von E-Mails genutzt werden soll – nicht aber zum Empfang. Das kann beispielsweise für Foren- oder Blogsoftware sinnvoll sein, die mit ihrem Account nur E-Mails verschicken soll.

### Alias-Tabelle

```
CREATE TABLE `aliases` (
    `id` int unsigned NOT NULL AUTO_INCREMENT,
    `source_username` varchar(64),
    `source_domain` varchar(255) NOT NULL,
    `destination_username` varchar(64) NOT NULL,
    `destination_domain` varchar(255) NOT NULL,
    `enabled` boolean DEFAULT '0',
    PRIMARY KEY (`id`),
    UNIQUE KEY (`source_username`, `source_domain`, `destination_username`, `destination_domain`),
    FOREIGN KEY (`source_domain`) REFERENCES `domains` (`domain`)
);
```

Die Alias-Tabelle enthält alle Weiterleitungen / Aliase und ist eigentlich selbsterklärend. Zur temporären Deaktivierung von Weiterleitungsadressen gibt es wieder ein “enabled”-Feld.

### TLS Policy-Tabelle

```
CREATE TABLE `tlspolicies` (
    `id` int unsigned NOT NULL AUTO_INCREMENT,
    `domain` varchar(255) NOT NULL,
    `policy` enum('none', 'may', 'encrypt', 'dane', 'dane-only', 'fingerprint', 'verify', 'secure') NOT NULL,
    `params` varchar(255),
    PRIMARY KEY (`id`),
    UNIQUE KEY (`domain`)
);
```

Mithilfe der TLS Policy Tabelle kann festgelegt werden, für welche Empfängerdomains bestimmte Sicherheitsbeschränkungen beim Mailtransport gelten sollen. Für einzelne Domains, z.B. “gmx.de” kann beispielsweise angegeben werden, dass diese E-Mails nur noch verschlüsselt übertragen werden dürfen. Mehr dazu später.

Die Datenbank wird mit Datensätzen befüllt, sobald die Server fertig konfiguriert sind. Bis dahin könnt ihr die MySQL-Kommandozeile mit `quit;` verlassen.

## vmail-Benutzer und -Verzeichnis einrichten

Alle Mailboxen werden direkt im Dateisystem des Debian Servers abgelegt. Für die Zugriffe auf die Mailbox-Verzeichnisse wird ein eigener Benutzer “vmail” (“Virtual Mail”) erstellt, unter dem die Zugriffe von Dovecot und anderen Komponenten des Mailservers geschehen sollen. Einerseits wird so verhindert, dass Mailserver-Komponenten auf sensible Systemverzeichnisse Zugriff bekommen, andererseits können wir so die Mailboxen vor dem Zugriff von außen schützen. Nur vmail (und root) dürfen auf die Mailboxen zugreifen.

Das Verzeichnis `/var/vmail/` soll alle Mailserver-relevanten Dateien (also Mailboxen und Filterscripts) enthalten und wird für den vmail-User als Home Directory festgelegt.

vmail-Benutzer erstellen:

```
useradd --create-home --home-dir /var/vmail --user-group --shell /usr/sbin/nologin vmail
```

vmail Unterverzeichnisse erstellen:

```
mkdir /var/vmail/mailboxes
mkdir -p /var/vmail/sieve/global
```

Verzeichnis `/var/vmail` rekursiv an vmail-User übereignen und Verzeichnisrechte passend setzen:

```
chown -R vmail /var/vmail
chgrp -R vmail /var/vmail
chmod -R 770 /var/vmail
```

## Dovecot installieren und konfigurieren

Nachdem die Datenbank und der vmail-User angelegt wurden, widmen wir uns nun dem Dovecot-Server. Wie bereits erwähnt, verwaltet dieser Server die Mailboxen und bekommt daher (in der Gestalt des vmail-Users) exklusiv Zugriff auf `/var/vmail/`. Zuerst müssen jedoch alle Serverkomponenten installiert werden:

```
apt install dovecot-core dovecot-imapd dovecot-lmtpd dovecot-mysql dovecot-sieve dovecot-managesieved
```

-   `dovecot-core`: Dovecot-Kern
-   `dovecot-imapd`: Fügt IMAP-Funktionalität hinzu
-   `dovecot-lmtp`: Fügt LMTP (Local Mail Transfer Protocol)-Funktionalität hinzu; LMTP wird als MTP-Protokoll zwischen Postfix und Dovecot genutzt
-   `dovecot-mysql`: Lässt Dovecot mit der MySQL-Datenbank zusammenarbeiten
-   `dovecot-sieve`: Fügt Filterfunktionalität hinzu
-   `dovecot-managesieved`: Stellt eine Schnittstelle zur Einrichtung der Filter via Mailclient bereit

Nach der Installation wird Dovecot automatisch gestartet. Beendet Dovecot, solange wir keine fertige Konfiguration haben:

```
systemctl stop dovecot
```

Nun geht es an die Konfiguration. Die Dovecot-Konfigurationsdateien liegen im Verzeichnis `/etc/dovecot/`. Dort könnt ihr schon einige Konfigurationen sehen, die bei der Installation angelegt wurden. Wir werden die Konfiguration von Grund auf neu aufsetzen - deshalb wird zuerst einmal die gesamte Dovecot-Konfiguration gelöscht:

```
rm -r /etc/dovecot/*
cd /etc/dovecot
```

Für Dovecot reichen die folgenden zwei Konfigurationsdateien (`dovecot.conf` und `dovecot-sql.conf`) aus. Erstellt die beiden Dateien im Verzeichnis `/etc/dovecot/`.

### Hauptkonfigurationsdatei `/etc/dovecot/dovecot.conf`

```
##
## Aktivierte Protokolle
##

protocols = imap lmtp sieve 


##
## TLS Config
## Quelle: https://ssl-config.mozilla.org/#server=dovecot&version=2.3.9&config=intermediate&openssl=1.1.1d&guideline=5.4
##

ssl = required
ssl_cert = </etc/acme.sh/mail.mysystems.tld/fullchain.pem
ssl_key = </etc/acme.sh/mail.mysystems.tld/privkey.pem
ssl_dh = </etc/dovecot/dh4096.pem
ssl_min_protocol = TLSv1.2
ssl_cipher_list = ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384
ssl_prefer_server_ciphers = no


##
## Dovecot services
##

service imap-login {
    inet_listener imap {
        port = 143
    }
}

service managesieve-login {
    inet_listener sieve {
        port = 4190
    }
}

service lmtp {
    unix_listener /var/spool/postfix/private/dovecot-lmtp {
        mode = 0660
        group = postfix
        user = postfix
    }

    user = vmail
}

service auth {
    ### Auth socket für Postfix
    unix_listener /var/spool/postfix/private/auth {
        mode = 0660
        user = postfix
        group = postfix
    }

    ### Auth socket für LMTP-Dienst
    unix_listener auth-userdb {
        mode = 0660
        user = vmail
        group = vmail
    }
}


##
##  Protocol settings
##

protocol imap {
    mail_plugins = $mail_plugins quota imap_quota imap_sieve
    mail_max_userip_connections = 20
    imap_idle_notify_interval = 29 mins
}

protocol lmtp {
    postmaster_address = postmaster@mysystems.tld
    mail_plugins = $mail_plugins sieve notify push_notification
}


##
## Client authentication
##

disable_plaintext_auth = yes
auth_mechanisms = plain login
auth_username_format = %Lu

passdb {
    driver = sql
    args = /etc/dovecot/dovecot-sql.conf
}

userdb {
    driver = sql
    args = /etc/dovecot/dovecot-sql.conf
}


##
## Address tagging
##
recipient_delimiter = +


##
## Mail location
##

mail_uid = vmail
mail_gid = vmail
mail_privileged_group = vmail

mail_home = /var/vmail/mailboxes/%d/%n
mail_location = maildir:~/mail:LAYOUT=fs


##
## Mailbox configuration
##

namespace inbox {
    inbox = yes

    mailbox Spam {
        auto = subscribe
        special_use = \Junk
    }

    mailbox Trash {
        auto = subscribe
        special_use = \Trash
    }

    mailbox Drafts {
        auto = subscribe
        special_use = \Drafts
    }

    mailbox Sent {
        auto = subscribe
        special_use = \Sent
    }
}


##
## Mail plugins
##

plugin {
    sieve_plugins = sieve_imapsieve sieve_extprograms
    sieve_before = /var/vmail/sieve/global/spam-global.sieve
    sieve = file:/var/vmail/sieve/%d/%n/scripts;active=/var/vmail/sieve/%d/%n/active-script.sieve

    ###
    ### Spam learning
    ###
    # From elsewhere to Spam folder
    imapsieve_mailbox1_name = Spam
    imapsieve_mailbox1_causes = COPY
    imapsieve_mailbox1_before = file:/var/vmail/sieve/global/learn-spam.sieve

    # From Spam folder to elsewhere
    imapsieve_mailbox2_name = *
    imapsieve_mailbox2_from = Spam
    imapsieve_mailbox2_causes = COPY
    imapsieve_mailbox2_before = file:/var/vmail/sieve/global/learn-ham.sieve

    sieve_pipe_bin_dir = /usr/bin
    sieve_global_extensions = +vnd.dovecot.pipe

    quota = maildir:User quota
    quota_exceeded_message = Benutzer %u hat das Speichervolumen überschritten. / User %u has exhausted allowed storage space.
}
```

Anzupassende Stellen:

-   `ssl_cert`: Pfad zur Zertifikatsdatei
-   `ssl_key`: Pfad zur Zertifikatsdatei
-   `postmaster_address`: Domain anpassen

#### Erklärung

`dovecot.conf` ist die Hauptkonfigurationsdatei des Dovecot-Servers:

**Dovecot Services:** Im darauf folgenden Abschnitt werden die Dovecot Services konfiguriert. Dazu gehört z.B. der Dienst “imap-login”, der auf eingehende Verbindungen von E-Mail Clients auf Port 143 horcht. Auch “managesieve-login” kommuniziert mit dem Mailclient, wenn dieser eine Funktion zur Bearbeitung Server-seitiger Filterscripte mitbringt. Die anderen Dienste werden intern genutzt: Der lmtp-Dienst stellt eine Schnittstelle bereit, über die Postfix empfangene Mails an die Mailbox übergeben kann. Der “auth” Dienst wird vom LMTP-Dienst genutzt, um die Existenz von Benutzern zu überprüfen, aber auch von Postfix, um den Login am Postfix-Server zu überprüfen. Mit “mode”, “user” und “group” wird bestimmt, welcher Systemuser Zugriff auf den Dienst haben soll (Analog zu den Dateirechten – der Socket für den Dienst ist nichts anderes als eine Datei).

**Protocol settings:** Für die verwendeten Protokolle können zusätzliche Einstellungen gesetzt werden – u.A. auch, welche Erweiterungen im Zusammenhang mit dem Protokoll genutzt werden sollen. “quota” und “imap_quota” sind notwendig, um das maximale Volumen einer Mailbox festsetzen zu können. Beim lmtp-Protokoll kann auf diese Erweiterungen verzichtet werden: Hier wird nur die Sieve-Erweiterung zum Filtern von E-Mails benötigt.

**Client Authentication:** Die Zeilen

```
disable_plaintext_auth = yes
auth_mechanisms = plain login
```

scheinen sich zu widersprechen, schließlich wird die Klartext-Authentifizierung abgeschaltet. Doch tatsächlich wird sie das nur für unverschlüsselte Verbindungen. TLS-Verschlüsselte Verbindungen bleiben davon unberührt, sodass in der nächsten Zeile die “plain” Authentifizierung mit Klartext-Passwörtern wieder angeboten werden kann. Das wird aus zwei Gründen getan:

-   “Klartext” tut uns hier nicht weh – schließlich ist die Verbindung sowieso (zwingend) verschlüsselt.
-   Alle Mailclients unterstützen die Klartextauthentifizierung. Andere Loginmechanismen werden weniger gut unterstützt und sind aufwendiger.

Wir konzentrieren uns deshalb auf die klassische Klartextauthentifizierung. Wie bereits erwähnt: Da unsere Verbindung ohnehin verschlüsselt ist, ist das in diesem Fall nicht sicherheitsrelevant.

Für `passdb` und `userdb` wird jeweils der Pfad zur SQL-Datei eingestellt. Dort befindt sich jeweils eine passende SQL-Query. Die “passdb” wird befragt, wenn es um die Authentifizierung von Usern geht, die “userdb”, wenn die Existenz eines bestimmten E-Mail Kontos überprüft werden soll, oder benutzerdefinierte Einstellungen geladen werden müssen, wie z.B. das Mailbox-Kontingent (“Quota”).

**Mail location:** In diesem Abschnitt wird definiert, unter welchem Systemuser Dovecot auf Dateisystem-Ebene mit E-Mails hantieren soll. Außerdem wird ein Pfad-Schema festgelegt, das bestimmt, nach welcher Struktur die Mailbox-Verzeichnisse angelegt werden sollen. %d steht für die Domain des Accounts und %n für den Benutzernamen vor dem @. Der Pfad zu einer Benutzermailbox lautet z.B.: `/var/vmail/mailboxes/mysystems.tld/admin/mail/`

**Mailbox Configuration:** In der Mailbox eines jeden Users soll sich standardmäßig ein “Spam”-Ordner befinden, in die ein passendes Sieve-Filterskript verdächtige E-Mails verschieben soll.

**Mail Plugins:** Hier werden die Details zu den Erweiterungen `sieve`, `quota` und `imapsieve` definiert. Das Script unter `sieve_before` wird für alle User (unabhängig von den eigenen Einstellungen) immer ausgeführt. Es hat die Aufgabe, durch Rspamd markierte Mails in den Spam-Ordner zu verschieben. `sieve_dir` definiert das Schema für den Ort, an dem benutzerdefinierte Scripts abgelegt werden. Das aktive Skript eines Nutzers soll jeweils über den symbolischen Link `active-script.sieve` zugänglich sein. Die `imapsieve` Einstellungen lassen den IMAP-Server Verschiebevorgängezwischen Mailbox-Ordnern erkennen, sodass Rspamd aus einer Neuordnung lernen kann.

### Diffie-Hellman Parameter für Dovecot generieren

In neueren Versionen generiert Dovecot die Diffie-Hellman-Parameter für TLS-Verbindungen nicht mehr selbst. Also müssen wir selbst Hand anlegen und die Parameter mittels OpenSSL-Tool generieren lassen:

```
openssl dhparam -out /etc/dovecot/dh4096.pem 4096 
```

Das kann je nach Auslastung des Mailservers durchaus eine viertel Stunde oder länger dauern. Um den Vorhang zu beschleunigen, kann ein sog. Entropy Harvester wie z.B. `haveged` installiert werden (`apt install haveged`).

### SQL-Konfgurationsdatei `/etc/dovecot/dovecot-sql.conf`

```
driver=mysql
connect = "host=localhost dbname=vmail user=vmail password=vmaildbpass"
default_pass_scheme = SHA512-CRYPT

password_query = SELECT username AS user, domain, password FROM accounts WHERE username = '%Ln' AND domain = '%Ld' and enabled = true;
user_query = SELECT concat('*:storage=', quota, 'M') AS quota_rule FROM accounts WHERE username = '%Ln' AND domain = '%Ld' AND sendonly = false;
iterate_query = SELECT username, domain FROM accounts where sendonly = false;
```

Anzupassende Stellen:

-   Datenbankpasswort “vmaildbpass”

`dovecot-sql.conf` enthält sensible Datenbank-Zugangsdaten und wird deshalb geschützt:

```
chmod 440 dovecot-sql.conf
```

#### Erklärung

Die Konfigurationsdatei `dovecot-sql.conf` enthält alle SQL-relevanten Einstellungen:

-   `driver`: Welcher Datenbank-Treiber soll genutzt werden?
-   `connect`: Informationen zur Datenbankverbindung
-   `default_pass_scheme`: Standardmäßig angenommenes Hash-Schema, wenn es in der Datenbank nicht explizit angegeben ist, z.B. mit vorangestelltem {SHA512-CRYPT}.
-   `password_query`: SQL Query für die Überprüfung des User-Logins. Stimmen Benutzername und Passwort überein? Existiert der Benutzer und ist er aktiviert?
-   `user_query`: SQL-Query zum Abholen aller Benutzer-spezifischen Einstellungen. In diesem Fall: Maximales Mailbox-Volumen (“Quota”).
-   `iterate_query`: SQL-Query zur Abfrage aller verfügbarer Benutzer. Benutzer, die keine Mails empfangen können (sendonly=true) sind für Dovecot nicht interessant und werden nicht mit ausgegeben.

### Globales Sieve-Filterscript für Spam

Unter `/var/vmail/sieve/global/` wird das Sieve-Filterscript `spam-global.sieve` erstellt, das erkannte Spammails in den Unterordner “Spam” jeder Mailbox einsortiert. Rspamd markiert erkannte E-Mails mit einem speziellen Spam-Header, den das Script erkennt. Inhalt von `spam-global.sieve`:

```
require "fileinto";

if header :contains "X-Spam-Flag" "YES" {
    fileinto "Spam";
}

if header :is "X-Spam" "Yes" {
    fileinto "Spam";
}
```

### Spam Learning mit Rspamd

Beim Verschieben von Spammails in den Spam-Ordner bzw. dem Herausverschieben falsch beurteilter Mails in den Posteingang soll ein Lernprozess von Rspamd ausgelöst werden, sodass der Filter aus falschen Einschätzungen lernt und so mit der Zeit immer besser wird.

Dazu werden zwei Sieve-Scripts in `/var/vmail/sieve/global/` angelegt:

`learn-spam.sieve`

```
require ["vnd.dovecot.pipe", "copy", "imapsieve"];
pipe :copy "rspamc" ["learn_spam"];
```

`learn-ham.sieve`

```
require ["vnd.dovecot.pipe", "copy", "imapsieve", "environment", "variables"];

if environment :matches "imap.mailbox" "*" {
    set "mailbox" "${1}";
}

if string "${mailbox}" "Trash" {
    stop;
}

pipe :copy "rspamc" ["learn_ham"];
```

Das `learn-ham.sieve` Script besitzt noch einen Check, der überprüft, ob eine E-Mail aus dem Spam in den Papierkorb verschoben wurde. In diesem Fall sollen die betroffenen Mails ja nicht wieder als “Ham” markiert werden, daher wird in so einem Fall die Ausführung des Lernvorgangs verhindert.

## Postfix installieren und konfigurieren

Für unseren Postfix-Server benötigen wir nur zwei Pakete: Das Kernpaket `postfix` und die Komponente `postfix-mysql`, die Postfix mit der MySQL-Datenbank kommunizieren lässt.

```
apt install postfix postfix-mysql
```

Während der Installation werdet ihr nach der “Allgemeinen Art der Konfiguration” gefragt. Wählt an dieser Stelle “Keine Konfiguration” und beendet den Postfix-Server wieder:

```
systemctl stop postfix
```

Im Postfix-Konfigurationsverzeichnis `/etc/postfix` befinden sich trotz unserer Wahl “Keine Konfiguration” ein paar Konfigurationsdateien, die zunächst entfernt werden:

```
cd /etc/postfix
rm -r sasl
rm master.cf main.cf.proto master.cf.proto
```

Legt dann folgende Dateien im Verzeichnis `/etc/postfix` an:

### `/etc/postfix/main.cf`

```
##
## Netzwerkeinstellungen
##

mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128
inet_interfaces = 127.0.0.1, ::1, 203.0.113.1, 2001:db8::1
myhostname = mail.mysystems.tld


##
## Mail-Queue Einstellungen
##

maximal_queue_lifetime = 1h
bounce_queue_lifetime = 1h
maximal_backoff_time = 15m
minimal_backoff_time = 5m
queue_run_delay = 5m


##
## TLS Einstellungen
## Quelle: https://ssl-config.mozilla.org/#server=postfix&version=3.4.8&config=intermediate&openssl=1.1.1d&guideline=5.4
##

### Allgemein
tls_preempt_cipherlist = no
tls_ssl_options = NO_COMPRESSION
tls_medium_cipherlist = ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384

### Ausgehende SMTP-Verbindungen (Postfix als Sender)
smtp_tls_security_level = dane
smtp_dns_support_level = dnssec
smtp_tls_policy_maps = proxy:mysql:/etc/postfix/sql/tls-policy.cf
smtp_tls_session_cache_database = btree:${data_directory}/smtp_scache
smtp_tls_ciphers = medium
smtp_tls_CAfile = /etc/ssl/certs/ca-certificates.crt

### Eingehende SMTP-Verbindungen
smtpd_tls_security_level = may
smtpd_tls_auth_only = yes
smtpd_tls_ciphers = medium
smtpd_tls_mandatory_protocols = !SSLv2, !SSLv3, !TLSv1, !TLSv1.1
smtpd_tls_protocols = !SSLv2, !SSLv3, !TLSv1, !TLSv1.1
smtpd_tls_session_cache_database = btree:${data_directory}/smtpd_scache
smtpd_tls_cert_file=/etc/acme.sh/mail.mysystems.tld/fullchain.pem
smtpd_tls_key_file=/etc/acme.sh/mail.mysystems.tld/privkey.pem
smtpd_tls_dh1024_param_file = /etc/postfix/dh2048.pem


##
## Lokale Mailzustellung an Dovecot
##

virtual_transport = lmtp:unix:private/dovecot-lmtp


##
## Spamfilter und DKIM-Signaturen via Rspamd
##

smtpd_milters = inet:localhost:11332
non_smtpd_milters = inet:localhost:11332
milter_protocol = 6
milter_mail_macros =  i {mail_addr} {client_addr} {client_name} {auth_authen}
milter_default_action = accept



##
## Server Restrictions für Clients, Empfänger und Relaying
## (im Bezug auf S2S-Verbindungen. Mailclient-Verbindungen werden in master.cf im Submission-Bereich konfiguriert)
##

### Bedingungen, damit Postfix als Relay arbeitet (für Clients)
smtpd_relay_restrictions =      reject_non_fqdn_recipient
                                reject_unknown_recipient_domain
                                permit_mynetworks
                                reject_unauth_destination


### Bedingungen, damit Postfix ankommende E-Mails als Empfängerserver entgegennimmt (zusätzlich zu relay-Bedingungen)
### check_recipient_access prüft, ob ein account sendonly ist
smtpd_recipient_restrictions = check_recipient_access proxy:mysql:/etc/postfix/sql/recipient-access.cf


### Bedingungen, die SMTP-Clients erfüllen müssen (sendende Server)
smtpd_client_restrictions =     permit_mynetworks
                                check_client_access hash:/etc/postfix/without_ptr
                                reject_unknown_client_hostname


### Wenn fremde Server eine Verbindung herstellen, müssen sie einen gültigen Hostnamen im HELO haben.
smtpd_helo_required = yes
smtpd_helo_restrictions =   permit_mynetworks
                            reject_invalid_helo_hostname
                            reject_non_fqdn_helo_hostname
                            reject_unknown_helo_hostname

# Clients blockieren, wenn sie versuchen zu früh zu senden
smtpd_data_restrictions = reject_unauth_pipelining


##
## Restrictions für MUAs (Mail user agents)
##

mua_relay_restrictions = reject_non_fqdn_recipient,reject_unknown_recipient_domain,permit_mynetworks,permit_sasl_authenticated,reject
mua_sender_restrictions = permit_mynetworks,reject_non_fqdn_sender,reject_sender_login_mismatch,permit_sasl_authenticated,reject
mua_client_restrictions = permit_mynetworks,permit_sasl_authenticated,reject


##
## MySQL Abfragen
##

proxy_read_maps =       proxy:mysql:/etc/postfix/sql/aliases.cf
                        proxy:mysql:/etc/postfix/sql/accounts.cf
                        proxy:mysql:/etc/postfix/sql/domains.cf
                        proxy:mysql:/etc/postfix/sql/recipient-access.cf
                        proxy:mysql:/etc/postfix/sql/sender-login-maps.cf
                        proxy:mysql:/etc/postfix/sql/tls-policy.cf

virtual_alias_maps = proxy:mysql:/etc/postfix/sql/aliases.cf
virtual_mailbox_maps = proxy:mysql:/etc/postfix/sql/accounts.cf
virtual_mailbox_domains = proxy:mysql:/etc/postfix/sql/domains.cf
local_recipient_maps = $virtual_mailbox_maps


##
## Sonstiges
##

### Maximale Größe der gesamten Mailbox (soll von Dovecot festgelegt werden, 0 = unbegrenzt)
mailbox_size_limit = 0

### Maximale Größe eingehender E-Mails in Bytes (50 MB)
message_size_limit = 52428800

### Keine System-Benachrichtigung für Benutzer bei neuer E-Mail
biff = no

### Nutzer müssen immer volle E-Mail Adresse angeben - nicht nur Hostname
append_dot_mydomain = no

### Trenn-Zeichen für "Address Tagging"
recipient_delimiter = +

### Keine Rückschlüsse auf benutzte Mailadressen zulassen
disable_vrfy_command = yes
```

Anzupassen:

-   `inet_interfaces`: IP-Adressen `203.0.113.1, 2001:db8::1` müssen durch eigene IPv4- (und optional IPv6)-Adresse ersetzt werden.
-   `myhostname`: Ersetzen durch eigenen Hostnamen
-   `smtpd_tls_cert_file`: Pfad zur Zertifikatsdatei
-   `smtpd_tls_key_file`: Pfad zur Zertifikatsdatei

#### Diffie-Hellman-Parameter für Postfix generieren

Neben Dovecot bekommt auch Postfix “von Hand generierte” DH-Parameter. Hier allerdings nur 2048 Bit starke, um zu älteren Mailservern kompatibel zu bleiben.

```
openssl dhparam -out /etc/postfix/dh2048.pem 2048
```

Wundert euch übrigens nicht über das `1024` in der Einstellung `smtpd_tls_dh1024_param_file` - das ist nur Teil des Namens und hat keine Bedeutung für die Schlüssellänge.

Wenn der Mailserver (entgegen meiner Empfehlung) nicht einen `mail.domain.tld` Hostnamen hat, sondern unter dem Domainnamen läuft (`domain.tld`), muss zur Konfiguration eine Zeile mit

```
mydestination =
```

(ohne Inhalt nach dem “=") hinzugefügt werden, sonst werden E-Mails an der falschen Stelle gespeichert.

#### Erklärung

**Netzwerkeinstellungen:**

-   `mynetworks`: Anfragen von diesen IP-Adressen / aus diesen IP-Adressbereichen werden von Postfix gesondert behandelt (Verwendung für “mynetworks” in den Restrictions). Üblicherweise werden hier die lokalen Adressbereiche und IP-Adressen aus dem eigenen Netz eingetragen, z.B. von anderen eigenen, vertrauenswürdigen Servern.
-   `inet_interfaces`: Auf diesen IP-Adressen soll Postfix seine Ports öffnen. Die IP-Adressen müssen an den eigenen Server angepasst werden.
-   `myhostname`: Der Hostname des Mailservers, wie er bei der Mailverarbeitung genutzt werden soll.

**Mail-Queue Einstellungen:**

E-Mails in Postfix werden “gequeued”, d.h. in eine Warteschlange eingetragen, die regelmäßig abgearbeitet wird. Wenn Mails nicht zustellbar sind, verbleiben sie eine gewisse Zeit in der Queue, bis ihre Lebenszeit abgelaufen ist, und sie aus der Queue entfernt werden. Der Absender der E-Mail bekommt dann eine entsprechende Nachricht, in der er über die Unzustellbarkeit informiert wird.

-   `maximal_queue_lifetime`: Lebensdauer einer normalen Nachricht in der Queue. Wenn eine E-Mail innerhalb einer Stunde nicht zugestellt werden konnte, wird sie aus der Queue entfernt und der Absender benachrichtigt.
-   `bounce_queue_lifetime`: Lebensdauer einer Unzustellbarkeits-Benachrichtigung in der Queue.
-   `maximal_backoff_time`: Maximale Zeit, die verstreichen darf, bis für eine E-Mail ein neuer Zustellversuch gestartet wird.
-   `minimal_backoff_time`: Zeit, die mindestens verstrichen sein muss, bis ein neuer Zustellversuch gestartet wird.
-   `queue_run_delay`: Intervall, in dem die Queue nach nicht zustellbaren E-Mails durchsucht wird.

**TLS-Einstellungen:**

Kompression wird abgeschaltet und (wie bei Dovecot) eine Cipherlist vorgegeben, sodass die bestmögliche Verschlüsselung zwischen Client und Server genutzt wird. Im ersten Teilabschnitt werden die “smtp”-spezifischen TLS-Einstellungen festgelegt – d.h. die Einstellungen, die Postfix als sendenden Kommunikationspartner (Mail-Client) betreffen.

-   `smtp_tls_security_level`: Standard-TLS-Policy, wenn sie in der Datenbank für die Empfängerdomain nicht anders spezifiziert wurde: “dane” kontrolliert zunächst, ob für den Empfängerserver ein TLSA-Eintrag (DANE) im DNS vorliegt. Wenn das der Fall ist, wird eine verschlüsselte Verbindung erzwungen und das vorgezeigte Serverzertifikat mittels TLSA-Eintrag verifiziert. Sollte kein TLSA-Eintrag verfügbar sein, fällt Postfix in die Policy “may” zurück und verschlüsselt nur, wenn der andere Server das unterstützt. Zertifikate werden dabei nicht validiert. Sollten vorhandene TLSA-Einträge ungültig sein, wird stattdessen die “encrypt” Policy genutzt, welche zwar zwingend verschlüsselt, aber Zertifikate ebenfalls nicht validiert. Mehr zu den TLS-Policies folgt später.
-   `smtp_dns_support_level`: DNSSEC-gesicherte DNS-Lookups aktiveren und nutzen, falls möglich
-   `smtpd_tls_policy_maps`: Verweist auf die SQL-Queries, mit denen Empfängerdomain-spezifische TLS-Einstellungen geladen werden
-   `smtp_tls_protocols`: Veraltete SSL/TLS-Protokolle werden deaktiviert

Nun zum zweiten TLS-Block: Dieser gilt für eingehende Verbindungen. Sowohl für andere Server, als auch Mailclients. Wieder werden SSL v2 und 3 deaktiviert und eine starke Cipherlist ausgewählt. Eingehende Verbindungen können verschlüsselt sein, müssen aber nicht.

**LMTP-Service:**

`virtual_transport` übermittelt verarbeitete, eingehende E-Mails an den LMTP-Service von Dovecot, der sich dann um die Einordnung der Mail in die passende Mailbox kümmert.

**Spamfilter und DKIM-Signaturen via Rspamd:**

Dieser Abschnitt definiert den Rspam-Daemon als Milter für ein- und ausgehende E-Mails. Eingehende E-Mails werden durch Rspamd auf ihre Seriosität geprüft - ausgehende werden mit einem DKIM-Schlüssel signiert.

**Server Restrictions:**

Die Blöcke unter “Server restrictions” sind besonders wichtig für die Sicherheit des Mailservers. Falsch eingestellt erlauben sie den unberechtigten Versand von E-Mails (Stichwort “Open Relay”). Der Mailserver wird dann als Spam-Schleuder missbraucht und landet sehr schnell auf einer Blacklist. Damit das nicht passiert, sollten die Restrictions (Beschränkungen) sorgfältig eingestellt und mit einem passenden Open Relay Detektor überprüft sein.

Die Restrictions werden in Leserichtung nacheinander abgearbeitet. Am Ende jeder Verarbeitung steht immer ein “permit” oder “reject”. Für das bessere Verständnis ein Beispiel:

```
smtpd_relay_restrictions =      reject_non_fqdn_recipient
                                reject_unknown_recipient_domain
                                permit_mynetworks
                                reject_unauth_destination
```

`smtpd_relay_restrictions` bestimmt die Bedingungen, unter der Postfix als Mail-Relay (“Vermittlungsstelle”) arbeitet. Unser Postfix soll nur in drei Fällen auf eingehende E-Mails reagieren:

-   Wenn ein Mailclient eine E-Mail via Postfix ins Internet schicken will
-   Wenn ein fremder Mailserver eine E-Mail an unseren Postfix schickt
-   Wenn vom Mailserver selbst aus eine Mail verschickt werden soll

Um den ersten Fall wird sich in der `master.cf` Datei gekümmert. Dort werden die Relay Restrictions im Submission-Bereich so überschrieben, dass Mailclients nicht am freien Versenden gehindert werden. Aktuell interessieren daher nur die letzten beiden Anfrage-Typen. Die erste Zeile der Restriction lautet `reject_non_fqdn_recipien`. Sollte die Empfängeradresse keine vollwertige E-Mail Adresse sein, wird die Anfrage an Postfix direkt mit einem `reject` abgewiesen. Alle anderen Checks finden dann nicht mehr statt. Das führt dazu, dass Postfix eine Weiterverarbeitung nur akzeptiert, wenn die zu verarbeitende E-Mail einen gültigen Empfänger hat. Ähnliches gilt für `reject_unknown_recipient_domain`: Wenn die Empfängerdomain keinen gültigen MX- oder A-Eintrag im DNS hat (und der Zielserver damit nicht feststeht), wird die E-Mail abgelehnt.

Die darauf folgende Zeile enthält die “Restriction” `permit_mynetwork`. Wenn der Anfragesteller lokal ist (bzw. seine IP in `mynetworks` vermerkt ist), wird er mit einem `permit` durchgewunken und die E-Mail wird weiter verarbeitet. Weitere Checks finden dann nicht statt. Sollte er nicht in mynetworks vermerkt sein, wird der letzte Check durchgeführt: `reject_unauth_destination` kann nur bestanden werden, wenn die zu verarbeitende E-Mail an eine Empfängeradresse dieses Mailsystems geht. Sollte bis zum Ende der restriction-Definition noch kein `permit` oder `reject` ausgelöst worden sein, wird automatisch ein `permit` ausgelöst und die jeweilige Aktion erlaubt.

Alle anderen Restriction-Definitionen funktionieren ähnlich: Die Kriterien werden nacheinander überprüft. Beginnt ein Kriterium mit einem `reject`, wird bei Zutreffen ein `reject` ausgelöst, beginnt es mit einem `permit`, wird ein `permit` ausgelöst. In beiden Fällen werden die nachfolgenden Kriterien nicht mehr überprüft.

-   `smtpd_relay_restrictions`: Kriterien, die überprüft werden, wenn Anfragen am Postfix-Server eintreffen (Von fremden Mailservern oder vom eigenen Server aus, z.B. via sendmail)
-   `smtpd_recipient_restrictions`: Kriterien, die zusätzlich zu den relay_restrictions geprüft werden. Nur bei bestehen der Checks wird eine E-Mail auf dem lokalen System angenommen und an die Empfänger-Mailbox geschickt. An dieser Stelle wird über eine SQL-Abfrage nachgefragt, ob ein bestimmter Empfänger E-Mails empfangen können soll (=> Siehe Option in der Datenbank, Accounts nur zum Versenden freizuschalten).
-   `smtpd_client-restrictions`: Kriterien, auf die hin andere Server überprüft werden, wenn Kontakt zum Postfix-Server hergestellt wird. (Müssen gültigen Hostnamen und Reverse-DNS-Eintrag haben)
-   `smtpd_helo_restrictions`: Fremde Server müssen zu Beginn ihren gültigen Hostnamen nennen.
-   `smtpd_data_restrictions`: Ungeduldige Server sind oft Spammer.

**MySQL-Abfragen:**

Hier sind die Pfade zu den übrigen SQL-Dateien angegeben, die Postfix benötigt, um Daten aus der Datenbank abfragen zu können.

### `/etc/postfix/master.cf`

```
# ==========================================================================
# service type  private unpriv  chroot  wakeup  maxproc command + args
#               (yes)   (yes)   (no)    (never) (100)
# ==========================================================================
###
### SMTP-Serverbindungen aus dem Internet
### Authentifizuerung hier nicht erlaubt (Anmeldung nur via smtps/submission!)
smtp      inet  n       -       y       -       1       smtpd     
    -o smtpd_sasl_auth_enable=no
###
### SMTPS Service (Submission mit implizitem TLS - ohne STARTTLS) - Port 465
### Für Mailclients gelten andere Regeln, als für andere Mailserver (siehe smtpd_ in main.cf)
###
smtps     inet  n       -       y       -       -       smtpd
    -o syslog_name=postfix/smtps
    -o smtpd_tls_wrappermode=yes
    -o smtpd_tls_security_level=encrypt
    -o smtpd_sasl_auth_enable=yes
    -o smtpd_sasl_type=dovecot
    -o smtpd_sasl_path=private/auth
    -o smtpd_sasl_security_options=noanonymous
    -o smtpd_client_restrictions=$mua_client_restrictions
    -o smtpd_sender_restrictions=$mua_sender_restrictions
    -o smtpd_relay_restrictions=$mua_relay_restrictions
    -o milter_macro_daemon_name=ORIGINATING
    -o smtpd_sender_login_maps=proxy:mysql:/etc/postfix/sql/sender-login-maps.cf
    -o smtpd_helo_required=no
    -o smtpd_helo_restrictions=
    -o cleanup_service_name=submission-header-cleanup
###
### Submission-Zugang für Clients (mit STARTTLS - für Rückwärtskompatibilität) - Port 587
###
submission inet n       -       y       -       -       smtpd
    -o syslog_name=postfix/submission
    -o smtpd_tls_security_level=encrypt
    -o smtpd_sasl_auth_enable=yes
    -o smtpd_sasl_type=dovecot
    -o smtpd_sasl_path=private/auth
    -o smtpd_sasl_security_options=noanonymous
    -o smtpd_client_restrictions=$mua_client_restrictions
    -o smtpd_sender_restrictions=$mua_sender_restrictions
    -o smtpd_relay_restrictions=$mua_relay_restrictions
    -o milter_macro_daemon_name=ORIGINATING
    -o smtpd_sender_login_maps=proxy:mysql:/etc/postfix/sql/sender-login-maps.cf
    -o smtpd_helo_required=no
    -o smtpd_helo_restrictions=
    -o cleanup_service_name=submission-header-cleanup
###
### Weitere wichtige Dienste für den Serverbetrieb
###
pickup    unix  n       -       y       60      1       pickup
cleanup   unix  n       -       y       -       0       cleanup
qmgr      unix  n       -       n       300     1       qmgr
tlsmgr    unix  -       -       y       1000?   1       tlsmgr
rewrite   unix  -       -       y       -       -       trivial-rewrite
bounce    unix  -       -       y       -       0       bounce
defer     unix  -       -       y       -       0       bounce
trace     unix  -       -       y       -       0       bounce
verify    unix  -       -       y       -       1       verify
flush     unix  n       -       y       1000?   0       flush
proxymap  unix  -       -       n       -       -       proxymap
proxywrite unix -       -       n       -       1       proxymap
smtp      unix  -       -       y       -       -       smtp
relay     unix  -       -       y       -       -       smtp
showq     unix  n       -       y       -       -       showq
error     unix  -       -       y       -       -       error
retry     unix  -       -       y       -       -       error
discard   unix  -       -       y       -       -       discard
local     unix  -       n       n       -       -       local
virtual   unix  -       n       n       -       -       virtual
lmtp      unix  -       -       y       -       -       lmtp
anvil     unix  -       -       y       -       1       anvil
scache    unix  -       -       y       -       1       scache
###
### Cleanup-Service um MUA header zu entfernen
###
submission-header-cleanup unix n - n    -       0       cleanup
    -o header_checks=regexp:/etc/postfix/submission_header_cleanup
```

Die `/etc/postfix/master.cf` Datei will ich euch nur im Groben erklären. Wichtig zu wissen ist, dass hier die Definition und Konfiguration der verschiedenen Postfix-Dienste wie z.B. smtpd (eingehende SMTP-Verbindungen) und smtp (ausgehende SMTP-Verbindungen) passiert. Gut zu erkennen ist, dass über ein `-o` weitere Parameter an einen Dienst übergeben werden. So beispielsweise beim `smtps`-Dienst, der auf Port 465 für die SMTP-Kommunikation mit den Mailclients bereitsteht: Die hier angegebenen Einstellungen z.B. zu `smtpd_relay_restrictions` überschreiben die Einstellungen in der main.cf – allerdings nur für diesen einen spezifischen Dienst! Ein gutes Beispiel ist die Einstellung `smtpd_tls_security_level=encrypt`, die im Submission-Block steht. In der `main.cf` hatten wir hier “may” definiert, um keine Server auszuschließen, die TLS nicht beherrschen. Da smtpd-Einstellungen aber sowohl für andere Server als auch für Mailclient gelten, wäre damit auch zu den Mailclients gesagt: “Ihr könnt verschlüsselte Verbindungen herstellen – müsst aber nicht”. Das wollen wir selbstverständlich nicht! Mailclients sollen eine verschlüsselte Verbindung herstellen müssen! Deshalb wird die smtpd-Einstellung speziell für den `smtps`-Dienst mithilfe der `-o` Option überschrieben und auf “encrypt” gesetzt.

Der `smtps` Service am Anfang der Datei ist der SMTP-Dienst, zu dem sich Mailclients später verbinden sollen. Eine Verbindung ist hier nur über direktes TLS (nicht StartTLS!) möglich. Für Clients, die sich zu Port 587 verbinden wollen, steht weiterhin der `submission` Service darunter bereit (auch wenn er in vielen Fällen nicht mehr notwendig sein sollte).

Für besseren Datenschutz wird der “Received”-Header (+ weitere Datenschutz-relevante Header) bei eingehenden E-Mails entfernt, wenn sie über den `smtps`-Port eintreffen. Die meisten E-Mail-Clients senden ihren Namen und die Version mit. Zusätzlich vermerkt Postfix bei eingehenden E-Mails, von welcher IP-Adresse die E-Mail stammt. Auf diese Informationen können wir verzichten, deshalb werden sie mithilfe eines kleinen zusätzlichen Dienstes `submission-header-cleanup` (am Ende der Konfiguration) aus der E-Mail gelöscht. Im `smtps`- und Submission-Bereich wird via `cleanup_service_name` festgelegt, dass bei eingehenden Mails auf diesen Services der Filter anzuwenden ist. Die Filterregeln befinden sich in der Datei `/etc/postfix/submission_header_cleanup`

### Header Cleanup Regeln

Unter `/etc/postfix/submission_header_cleanup` wird eine Datei mit folgendem Inhalt angelegt:

```
### Entfernt Datenschutz-relevante Header aus E-Mails von MTUAs

/^Received:/            IGNORE
/^X-Originating-IP:/    IGNORE
/^X-Mailer:/            IGNORE
/^User-Agent:/          IGNORE
```

### SQL-Konfiguration

Neben der Haupt-Konfiguration main.cf und der Service-Konfiguration master.cf werden noch ein paar Konfigurationsdateien innerhalb des Unterverzeichnisses `sql/` angelegt, die die SQL-Queries für die Datenabfragen an die Datenbank enthalten:

```
mkdir /etc/postfix/sql && cd $_
```

Erstellt dann die folgenden Konfigurationsdateien mit dem zugehörigen Inhalt:

`accounts.cf`

```
user = vmail
password = vmaildbpass
hosts = unix:/run/mysqld/mysqld.sock
dbname = vmail
query = select 1 as found from accounts where username = '%u' and domain = '%d' and enabled = true LIMIT 1;
```

`aliases.cf`

```
user = vmail
password = vmaildbpass
hosts = unix:/run/mysqld/mysqld.sock
dbname = vmail
query = SELECT DISTINCT concat(destination_username, '@', destination_domain) AS destinations FROM aliases
        WHERE (source_username = '%u' OR source_username IS NULL) AND source_domain = '%d'
        AND enabled = true
        AND NOT EXISTS (SELECT id FROM accounts WHERE username = '%u' and domain = '%d');
```

`domains.cf`

```
user = vmail
password = vmaildbpass
hosts = unix:/run/mysqld/mysqld.sock
dbname = vmail
query = SELECT domain FROM domains WHERE domain='%s';
```

`recipient-access.cf`

```
user = vmail
password = vmaildbpass
hosts = unix:/run/mysqld/mysqld.sock
dbname = vmail
query = select if(sendonly = true, 'REJECT', 'OK') AS access from accounts where username = '%u' and domain = '%d' and enabled = true LIMIT 1;
```

`sender-login-maps.cf`

```
user = vmail
password = vmaildbpass
hosts = unix:/run/mysqld/mysqld.sock
dbname = vmail
query = select concat(username, '@', domain) as 'owns' from accounts where username = '%u' AND domain = '%d' and enabled = true union select 
        concat(destination_username, '@', destination_domain) AS 'owns' from aliases 
        where source_username = '%u' and source_domain = '%d' and enabled = true;
```

`tls-policy.cf`

```
user = vmail
password = vmaildbpass
hosts = unix:/run/mysqld/mysqld.sock
dbname = vmail
query = SELECT policy, params FROM tlspolicies WHERE domain = '%s';
```

**Vergesst nicht, `vmaildbpass` in jeder der Dateien durch euer eigenes Passwort zu ersetzen!**

Alle SQL-Konfgurationsdateien in `/etc/postfix/sql` werden vor dem Zugriff durch unberechtigte User geschützt:

```
chown -R root:postfix /etc/postfix/sql
chmod g+x /etc/postfix/sql
```

### Weitere Postfix-Konfigurationsdateien

Außerdem gibt es noch eine weitere Datei `/etc/postfix/without_ptr`, die zunächst leer bleiben kann:

```
touch /etc/postfix/without_ptr
```

Die Datei kann später einmal Einträge wie den folgenden beinhalten:

```
[2001:db8::beef] OK
```

Der Server mit der IP `2001:db8::beef` muss dann keinen gültigen PTR-Record (Reverse DNS) mehr besitzen und wird trotzdem akzeptiert. Die `without_ptr`-Datei muss dann nach jeder Änderung in eine Datenbankdatei umgewandelt und Postfix neu geladen werden:

```
postmap /etc/postfix/without_ptr
systemctl reload postfix
```

Im Moment reicht es aber aus, einfach nur eine leere Datenbankdatei zu generieren:

```
postmap /etc/postfix/without_ptr
```

Zum Schluss wird einmal

```
newaliases
```

ausgeführt, um die Alias-Datei `/etc/aliases.db` zu generieren, die Postfix standardmäßig erwartet.

## Rspamd

Da die Rspamd-Pakete für Debian nicht besonders aktuell sind und [offiziell davon abgeraten wird](https://rspamd.com/downloads.html#debian-standard-repos-notes), diese zu nutzen, nutzen wir an dieser Stelle das Debian-Repository des Rspamd-Projekts:

```
apt install -y lsb-release wget
wget -O- https://rspamd.com/apt-stable/gpg.key | apt-key add -
echo "deb http://rspamd.com/apt-stable/ $(lsb_release -c -s) main" > /etc/apt/sources.list.d/rspamd.list
echo "deb-src http://rspamd.com/apt-stable/ $(lsb_release -c -s) main" >> /etc/apt/sources.list.d/rspamd.list
```

Paketquellen aktualisieren und Rspamd installieren

```
apt update
apt install rspamd
```

Rspamd stoppen:

```
systemctl stop rspamd
```

![Rspamd Webinterface](https://thomas-leister.de/mailserver-debian-buster/images/rspamd-webinterface.png)

Rspamd Webinterface

### Grundkonfiguration

Die Konfiguration von Rspamd wird im Verzeichnis `/etc/rspamd/local.d/` abgelegt. Die folgenden Konfigurationsdateien werden darin erstellt:

`/etc/rspamd/local.d/worker-controller.inc`: Einstellung des Worker controllers: Passwort für den Zugriff via Weboberfläche, z.B.:

```
password = "$2$qecacwgrz13owkag4gqcy5y7yeqh7yh4$y6i6gn5q3538tzsn19ojchuudoauw3rzdj1z74h5us4gd3jj5e8y";
```

Der Passworthash (`$2$qecacwg...`) wird via

```
rspamadm pw
```

generiert und in die Datei eingefügt. Vergesst nicht das abschließende `";`!

`/etc/rspamd/local.d/logging.inc`: Error logging

```
type = "syslog";
level = "warning";
```

Milter Headers `/etc/rspamd/local.d/milter_headers.conf`

```
use = ["x-spamd-bar", "x-spam-level", "authentication-results"];
authenticated_headers = ["authentication-results"];
```

Redis für den Bayes’schen Filter nutzen: `/etc/rspamd/local.d/classifier-bayes.conf`

```
backend = "redis";
```

…und in `/etc/rspamd/local.d/redis.conf`:

```
servers = "127.0.0.1";
```

Für den Bayes’schen Filter (Textanalyse) wird “Auto-Learning” aktiviert:

`/etc/rspamd/override.d/classifier-bayes.conf`:

```
autolearn = true;
```

Wird eine E-Mail bereits beim Empfang abgelehnt, weil sie ausgrund der Metadaten offensichtlich von einem Spammer kommt, nutzt Rspamd die Gelegenheit und lernt, dass der Text in dieser E-Mail als Spam einzustufen ist. So wird die Erkennungsrate mit jeder Spammail besser. ([https://rspamd.com/doc/configuration/statistic.html](https://rspamd.com/doc/configuration/statistic.html))

### Manuell gepflegte Black-/Whitelists

Über das Multimap-Modul kann das Verhalten von Rspamd für bestimmte E-Mail-Merkmale personalisiert gesteuert werden. Merkmale können zum Beispiel die Absender-IP-Adresse oder die Absendermailadresse sein. Für beide registrieren wir in `/etc/rspamd/local.d/multimap.conf` jeweils eine Black- und eine Whitelist:

```
WHITELIST_IP {
    type = "ip";
    map = "$CONFDIR/local.d/whitelist_ip.map";
    description = "Local ip whitelist";
    action = "accept";
}

WHITELIST_FROM {
        type = "from";
        map = "$CONFDIR/local.d/whitelist_from.map";
        description = "Local from whitelist";
        action = "accept";
}

BLACKLIST_IP {
        type = "ip";
        map = "$CONFDIR/local.d/blacklist_ip.map";
        description = "Local ip blacklist";
        action = "reject";
}

BLACKLIST_FROM {
        type = "from";
        map = "$CONFDIR/local.d/blacklist_from.map";
        description = "Local from blacklist";
        action = "reject";
}
```

Für alle vier Listen werden nun Listendateien erstellt:

```
cd /etc/rspamd/local.d
touch whitelist_ip.map
touch whitelist_from.map
touch blacklist_ip.map
touch blacklist_from.map
cd - 
```

“IP”-Listen können IPv6- und IPv4-Adressen bzw. Adressbereiche enthalten - in jeder Zeile ein Eintrag. “From”-Listen enthalten vollständige Absendermailadressen. Die Listen können zunächst leer bleiben. Sie eignen sich gut, wenn man später einmal für einzelne Absender oder Server Ausnahmen einstellen möchte.

### DKIM Signing

Rspamd übernimmt auch das Signieren von ausgehenden E-Mails. Damit signiert werden kann, muss zunächst ein Signing Key generiert werden. Der Parameter `-s 2020` gibt den sogenannten Selektor an - einen Namen für den Key (hier das Erstellungsjahr).

```
mkdir /var/lib/rspamd/dkim/
rspamadm dkim_keygen -b 2048 -s 2020 -k /var/lib/rspamd/dkim/2020.key > /var/lib/rspamd/dkim/2020.txt
chown -R _rspamd:_rspamd /var/lib/rspamd/dkim
chmod 440 /var/lib/rspamd/dkim/*
```

Zum Signing Key (`/var/lib/rspamd/dkim/2020.key`) gehört ein dazu passender Public Key, welcher in Form eines vorbereiteten DNS-Records in der Datei `/var/lib/rspamd/dkim/2020.txt` liegt.

DKIM Record ausgeben lassen:

```
cat /var/lib/rspamd/dkim/2020.txt
```

Die Ausgabe sieht z.B. so aus:

```
2020._domainkey IN TXT ( "v=DKIM1; k=rsa; "
    "p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2/al5HqXUpe+HUazCr6t9lv2VOZLR369PPB4t+dgljZQvgUsIKoYzfS/w9NagS32xZYxi1dtlDWuRfTU/ahHO2MYzE0zHE4lMfwb6VkNCG+pM6bAkCwc5cFvyRygwxAPEiHAtmtU5b0i9LY25Z/ZWgyBxEWZ0Wf+hLjYHvnvMqewPsduUqKVjDOdUqeBb1VAu3WFErOAGVUYfKqFX"
    "+yfz36Alb7/OMAort8A5Vo5t5k0vxTHzkYYg5KB6tLS8jngrNucGjyNL5+k0ijPs3yT7WpTGL3U3SEa8cX8WvOO1fIpWQz4yyZJJ1Mm62+FskSc7BHjdiMHE64Id/UBDDVjxwIDAQAB"
) ;
```

Der Werte-Abschnitt des Records (beginnend mit `v=DKIM1` bis zum Ende der Zeichenkolonne - hier `AQAB`) muss in einen neuen DNS-Record gepflanzt werden. Dabei werden Zeilenumbrüche und Anführungsstriche entfernt. Je nach DNS-Hoster muss ein neuer Eintrag geringfügig anders formatiert werden. Ich habe den Schritt im Screenshot beispielhaft für den Hoster [Core-Networks.de](https://www.core-networks.de/) mit dem Selector “2020” und meiner Beispieldomain “mysystems.tld” durchgeführt:

![core-networks.de Screenshot mit DKIM Record](https://thomas-leister.de/mailserver-debian-buster/images/corenetworks-dkim.png)

core-networks.de Screenshot mit DKIM Record

Wichtig: Der Selektor “2020” wird im DNS-Record zusammen mit `._domainkey` als Name verwendet! Der DKIM-Record muss **für jede verwendete Domain (domain2.tld, domain2.tld) im jeweiligen Zonefile erstellt werden!**

Sollte der Record vom DNS-Hoster nicht akzeptiert werden, hilft es in einigen Fällen, die Schlüssellänge von 2048 Bit auf 1024 Bit zu reduzieren. Dazu das `rspamadm dkim_keygen` Kommando nochmals mit `-b 1024` statt mit `-b 2048` ausführen.

Der erzeugte DKIM-Key und der verwendete Selektor werden in der Konfigurationsdatei `/etc/rspamd/local.d/dkim_signing.conf` angegeben:

```
path = "/var/lib/rspamd/dkim/$selector.key";
selector = "2020";

### Enable DKIM signing for alias sender addresses
allow_username_mismatch = true;
```

Diese Konfiguration wird in die Datei `/etc/rspamd/local.d/arc.conf` kopiert, sodass das [ARC-Modul](https://rspamd.com/doc/modules/arc.html) korrekt arbeiten kann. Es greift auf dieselben Einstellungen zurück:

```
cp -R /etc/rspamd/local.d/dkim_signing.conf /etc/rspamd/local.d/arc.conf
```

## Redis als Cache und Key-Value Store für Rspamd-Module

Rspamd verwendet Redis als Cache. Die Installation ist trivial:

```
apt install redis-server
```

In der Rspamd-Konfiguration wurde Redis bereits als Caching-Datenbank eingetragen.

## Rspamd starten

Rspamd kann nun gestartet werden:

```
systemctl start rspamd
```

## Nginx Proxy für Rspamd Weboberfläche

Für den bequemen und sicheren Zugriff auf die Rspamd-Weboberfläche kann dieser ein Nginx HTTP-Proxy vorgeschaltet werden. Nginx kümmert sich dann um die Absicherung der Verbindung via HTTPS. Wer nur selten auf die Rspamd-Weboberfläche zugreift, kann auf diesen Schritt verzichten und stattdessen auch über einen SSH-Tunnel auf das Interface zugreifen ([siehe unten](https://thomas-leister.de/mailserver-debian-buster/#ssh-tunnel)).

Für den Rspamd-Webproxy wird in `/etc/nginx/sites-available/mail.mysystems.tld` ein `location` Block wie folgt hinzugefügt:

```
server {
        listen 80;
        listen [::]:80;
        listen 443 ssl http2;
        listen [::]:443 ssl http2;

        server_name mail.mysystems.tld imap.mysystems.tld smtp.mysystems.tld;

        ssl_certificate /etc/acme.sh/mail.mysystems.tld/fullchain.pem;
        ssl_certificate_key /etc/acme.sh/mail.mysystems.tld/privkey.pem;

        add_header Strict-Transport-Security max-age=15768000;

        location /rspamd/ {
                proxy_pass http://localhost:11334/;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        if ($ssl_protocol = "") {
            return 301 https://$server_name$request_uri;
        }
}
```

Anzupassen:

-   ssl_certificate: Pfad zu Zertifikat
-   ssl_certificate_key: Pfad zu Zertifikat
-   server_name

Konfiguration testen und Nginx neu laden:

```
nginx -t
systemctl reload nginx
```

## Weboberfläche aufrufen

Unter [https://mail.mysystems.tld/rspamd/](https://mail.mysystems.tld/rspamd/) ist die Rspamd-Weboberfläche nun erreichbar. Als Passwort wird das weiter oben erzeugte Passwort für die Weboberfläche verwendet.

## Via SSH-Tunnel mit der Weboberfläche verbinden (Alternative)

Statt über Nginx kann man auch mithilfe eines SSH-Tunnels eine sichere Verbindung zur Rspamd-Weboberfläche aufbauen. Dazu benötigt man auf dem lokalen Rechner allerdings einen SSH-Client. Der SSH-Befehl

```
ssh -L 8080:localhost:11334 benutzer@mail.mysystems.tld -N
```

verknüpft den Port des Webinterfaces (`11334`) mit Port `8080` des lokalen Systems. Im lokalen Webbrowser kann die Oberfläche nun unter http://localhost:8080 erreicht werden. Mit STRG+C wird die Verbindung wieder getrennt.

## Rspamd mit bestehenden Spam-E-Mails trainieren (optional)

Wer einige Mails im Maildir-Format (jede E-Mail ist eine Datei) vorliegen hat, kann Rspamd mit über das rspamc-Werkzeug trainieren. Dabei ist es ist vorteilhaft, nicht nur Spammail-Beispiele zu trainieren, sondern auch Beispiele für erwünschte E-Mails. Im folgenden Beispiel wurde das Mailbox-Verzeichnis eines älteren Mailservers importiert:

E-Mails in einem Verzeichnis als **Spam** antrainieren:

```
find ./oldserver/var/vmail/mailboxes/*/*/mail/Spam/cur -type f -exec /usr/bin/rspamc learn_spam {} \;
```

E-Mails in einem Verzeichnis als **Ham** (harmlos) antrainieren:

```
find ./oldserver/var/vmail/mailboxes/*/*/mail/cur -type f -exec /usr/bin/rspamc learn_ham {} \;
find ./oldserver/var/vmail/mailboxes/*/*/mail/Sent/cur -type f -exec /usr/bin/rspamc learn_ham {} \;
```

Auf der Rspamd-Weboberfläche wird nach dem Training eine entsprechend höhere Anzahl an gelernten E-Mails angezeigt.

## Autoconfig für Mozilla Thunderbird (Optional)

Mozilla Thunderbird (und andere Mailclients) versuchen bei der Einrichtung eines neuen Mailkontos automatisch, die korrekten Adressen und Einstellungen für IMAP- und SMTP-Server zu [ermitteln](https://developer.mozilla.org/en-US/docs/Mozilla/Thunderbird/Autoconfiguration). Die Autokonfiguration gibt uns die Möglichkeit, unter einer festgelegten Adresse `https://autoconfig.<maildomain>.tld/mail/config-v1.1.xml` Informationen zum Mailserver zu hinterlegen, sodass der Benutzer bei der Verknüpfung seines Mailkontos nichts anderes als seine Mailadresse und das Passwort anzugeben braucht. Alle weiteren Informationen wie z.B. Art der Verschlüsselung oder Port bezieht Thunderbird aus der XML-Datei.

Da die Servereinstellungen in diesem Setup für alle Domains identisch sind, soll die XML-Datei unter `https://autoconfig.mysystems.tld/mail/config-v1.1.xml` zentral auf dem Mailserver verfügbar gemacht werden. Sollten neben der “mysystems.tld” Domain noch die Domains “domain1.tld” und “domain2.tld” für E-Mail mitgenutzt werden, kann mittels HTTP-Proxies auf den Zielservern dieser Domains auf die zentrale Adresse weitergeleitet werden. Doch zunächst soll es nur um den mail.mysystems.tld Mailserver gehen …

### DNS-Record anlegen

Für die neue autoconfig.mysystems.tld Subdomain wird ein passender CNAME-Record im DNS angelegt, welcher auf den Mailserver zeigt:

```
autoconfig.mysystems.tld. 86400 IN CNAME mail.mysystems.tld.
```

### Autoconfig auf dem Mailserver einrichten

Um die Datei auf dem Server anzubieten, wird ein weiterer Virtual Host für den Nginx-Webserver angelegt:

`/etc/nginx/sites-available/autoconfig.mysystems.tld`

```
server {
        listen 80;
        listen [::]:80;
#        listen 443 ssl http2;
#        listen [::]:443 ssl http2;

        server_name autoconfig.mysystems.tld;

#        ssl_certificate /etc/acme.sh/autoconfig.mysystems.tld/fullchain.pem;
#        ssl_certificate_key /etc/acme.sh/autoconfig.mysystems.tld/privkey.pem;

#        add_header Strict-Transport-Security max-age=15768000;

#        if ($ssl_protocol = "") {
#            return 301 https://$server_name$request_uri;
#        }

        root /var/www/mysystems.tld/autoconfig.mysystems.tld;

        location / {
                add_header Content-Type text/xml;
                charset utf-8;
        }
}
```

_Wie auch bei der ersten Nginx-Konfiguration sind hier zunächst ein paar Zeilen auskommentiert, weil noch keine passenden TLS-Zertifikate vorhanden sind._

Konfiguration aktivieren, Nginx Config prüfen und neu laden:

```
ln -s /etc/nginx/sites-available/autoconfig.mysystems.tld /etc/nginx/sites-enabled/autoconfig.mysystems.tld
nginx -t
systemctl reload nginx
```

Für den neuen vHost wird ein Webroot directory angelegt:

```
mkdir -p /var/www/mysystems.tld/autoconfig.mysystems.tld/mail/
```

und die XML-Konfiguration darin abgelegt:

`config-v1.1.xml`

```
<?xml version="1.0" encoding="UTF-8"?>

<clientConfig version="1.1">
  <emailProvider id="mysystems.tld">
    <domain>mysystems.tld</domain>
    <displayName>mysystems.tld Mail</displayName>
    <displayShortName>mysystems.tld</displayShortName>
    <incomingServer type="imap">
      <hostname>imap.mysystems.tld</hostname>
      <port>993</port>
      <socketType>SSL</socketType>
      <authentication>password-cleartext</authentication>
      <username>%EMAILADDRESS%</username>
    </incomingServer>
    <outgoingServer type="smtp">
      <hostname>smtp.mysystems.tld</hostname>
      <port>465</port>
      <socketType>SSL</socketType>
      <authentication>password-cleartext</authentication>
      <username>%EMAILADDRESS%</username>
    </outgoingServer>
  </emailProvider>
</clientConfig>
```

Nun wird für autoconfig.mysystems.tld noch ein DNS-Record angelegt:

```
autoconfig.mysystems.tld IN CNAME mail.mysystems.tld.
```

TLS-Zertifikat beantragen und installieren:

```
acme.sh --issue --server letsencrypt --nginx -d autoconfig.mysystems.tld
mkdir -p /etc/acme.sh/autoconfig.mysystems.tld
acme.sh --install-cert -d autoconfig.mysystems.tld \
    --key-file /etc/acme.sh/autoconfig.mysystems.tld/privkey.pem  \
    --fullchain-file /etc/acme.sh/autoconfig.mysystems.tld/fullchain.pem \
    --reloadcmd "systemctl reload nginx"
```

**Die auskommentierten Zeilen können nun entfernt und Nginx neu geladen werden:**

```
systemctl reload nginx
```

### Optional: Autoconfig Proxy für weitere Maildomains einrichten

Auf den (Web-)Servern, auf welche die weiteren Domains “domain1.tld” und “domain2.tld” verweisen, wird im Nginx jeweils ein vHost für “autoconfig.domain1.tld” bzw. “autoconfig.domain2.tld” angelegt:

`/etc/nginx/sites-available/autoconfig.domain1.tld`

```
server {
        listen 80;
        listen [::]:80;
#       listen 443 ssl http2;
#       listen [::]:443 ssl http2;

        server_name autoconfig.domain1.tld;

#       ssl_certificate /etc/acme.sh/autoconfig.mysystems.tld/fullchain.pem;
#       ssl_certificate_key /etc/acme.sh/autoconfig.mysystems.tld/key.pem;

#       add_header Strict-Transport-Security max-age=15768000;

#       if ($ssl_protocol = "") {
#           return 301 https://$server_name$request_uri;
#       }      

        location / {
                proxy_pass https://[fd80::1]:443;
                proxy_set_header HOST $host;
        }
}
```

Anzupassen:

-   `server_name`
-   IP-Adresse des Mailsystems `mail.mysytems.tld` bei `proxy_pass`

_Die `proxy_pass` Anweisung nutzt die IPv6-Adresse `fd::80` statt des Hostnamens unseres Mailservers, da Nginx direkt nach dem Booten noch keinen DNS-Resolver zur Namensauflösung verfügbar hat._

Ein DNS-Eintrag für die neue Subdomain darf nicht fehlen:

```
autoconfig.domain1.tld IN CNAME domain1.tld.
```

Auch dieser VirtualHost sollte mit einem passenden TLS-Zertifikat abgesichert werden:

```
acme.sh --issue --server letsencrypt --nginx -d autoconfig.domain1.tld
mkdir -p /etc/acme.sh/autoconfig.domain1.tld
acme.sh --install-cert -d autoconfig.domain1.tld \
    --key-file /etc/acme.sh/autoconfig.domain1.tld/privkey.pem  \
    --fullchain-file /etc/acme.sh/autoconfig.domain1.tld/fullchain.pem \
    --reloadcmd "systemctl reload nginx"
```

Die auskommentierten Zeilen in der Nginx Konfiguration können nun auskommentiert werden.

Aktivieren der Konfiguration und Neuladen des Webservers:

```
ln -s /etc/nginx/sites-available/autoconfig.domain1.tld /etc/nginx/sites-enabled/autoconfig.domain1.tld
nginx -t
systemctl reload nginx
```

Ein Aufruf von [https://autoconfig.domain1.tld/mail/config-v1.1.xml](https://autoconfig.domain1.tld/mail/config-v1.1.xml) sollte nun dieselbe XML-Datei anzeigen, die bereits auf dem Mailserver unter `autoconfig.mysystems.tld` hinterlegt wurde. Diese XML-Datei muss nun analog zu `mysystems.tld` um `domain1.tld` erweitert werden, z.B. so:

```
<?xml version="1.0" encoding="UTF-8"?>

<clientConfig version="1.1">
  <emailProvider id="mysystems.tld">
    <domain>mysystems.tld</domain>
    <displayName>mysystems.tld Mail</displayName>
    <displayShortName>mysystems.tld</displayShortName>
    <incomingServer type="imap">
      <hostname>imap.mysystems.tld</hostname>
      <port>993</port>
      <socketType>SSL</socketType>
      <authentication>password-cleartext</authentication>
      <username>%EMAILADDRESS%</username>
    </incomingServer>
    <outgoingServer type="smtp">
      <hostname>smtp.mysystems.tld</hostname>
      <port>465</port>
      <socketType>SSL</socketType>
      <authentication>password-cleartext</authentication>
      <username>%EMAILADDRESS%</username>
    </outgoingServer>
  </emailProvider>

  <emailProvider id="domain1.tld">
    <domain>domain1.tld</domain>
    <displayName>domain1.tld Mail</displayName>
    <displayShortName>domain1.tld</displayShortName>
    <incomingServer type="imap">
      <hostname>imap.mysystems.tld</hostname>
      <port>993</port>
      <socketType>SSL</socketType>
      <authentication>password-cleartext</authentication>
      <username>%EMAILADDRESS%</username>
    </incomingServer>
    <outgoingServer type="smtp">
      <hostname>smtp.mysystems.tld</hostname>
      <port>465</port>
      <socketType>SSL</socketType>
      <authentication>password-cleartext</authentication>
      <username>%EMAILADDRESS%</username>
    </outgoingServer>
  </emailProvider>
</clientConfig>
```

Für “domain2.tld” ist genauso vorzugehen.

## Domains, Accounts, Aliase und TLS-Policies in Datenbank definieren

Bevor der Mailserver sinnvoll genutzt werden kann, müssen noch Domains und Benutzer im der MySQL-Datenbank registriert werden. Loggt euch wieder auf der MySQL-Kommandozeile ein:

```
mysql
```

… und wechselt in die vmail-Datenbank:

```
use vmail;
```

### Neue Domain anlegen

Damit ein neuer Benutzeraccount oder ein neuer Alias angelegt werden kann, muss die zu nutzende Domain zuvor im Mailsystem bekannt gemacht werden. Postfix verarbeitet nur E-Mails an Domains, die in der “domains”-Tabelle eingetragen sind:

```
insert into domains (domain) values ('mysystems.tld');
```

### Neuen E-Mail-Account anlegen

Wenn die Benutzerdomain in der Domain-Tabelle angelegt ist, kann ein neuer Benutzeraccount für den Mailserver erstellt werden. Bevor das passende SQL-Kommando eingegeben und abgeschickt wird, wird jedoch zu nächst ein Passwort-Hash des gewünschten Passworts für den Account erzeugt. Mit

```
doveadm pw -s SHA512-CRYPT
```

**(in der Bash Shell! - Nicht in der MySQL Shell!)** kann ein solcher Hash erzeugt werden. Beispiel für einen ausgegebenen Hash:

```
{SHA512-CRYPT}$6$wHyJsS.doo39xoCu$KI1N4l.Vd0ZWYj5BYLI8AdK7ACwAZaM18gSy7Bko0dG2Hvli4.KfAmLk2ztFVP.R4T7oqiu7clKBehCTc4GGw0
```

Dieser Hash ist für jedes Passwort einzigartig und ändert sich sogar bei jeder Generierung. Legt den Hash am besten gleich in eurer Zwischenablage oder einem Textdokument ab - ihr benötigt ihn gleich!

Verwendet auch an dieser Stelle möglichst nur die Zeichen 0-9, a-z und A-z. Sonderzeichen können Probleme verursachen. Wenn eure Passwörter einigermaßen lang sind, reicht das völlig aus. Sonderzeichen bringen dann ohnehin keinen nennenswerten Sicherheitsgewinn.

Das SQL-Kommando zum Erzeugen eines neuen Accounts lautet:

```
insert into accounts (username, domain, password, quota, enabled, sendonly) values ('user1', 'mysystems.tld', '{SHA512-CRYPT}$6$wHyJsS[...]', 2048, true, false);
```

In das “Password”-Feld wird der Hash vollständig eingetragen (hier: gekürzt).

Legt am besten gleich den `postmaster@mysystems.tld` Account an. Er sollte auf jedem Mailserver vorhanden sein, um den Administrator bei technischen Problemen mit dem Server erreichen zu können.

### Neuen Alias anlegen

```
insert into aliases (source_username, source_domain, destination_username, destination_domain, enabled) values ('alias', 'mysystems.tld', 'user1', 'mysystems.tld', true);
```

… legt einen Alias für den Benutzer “[user1@mysystems.tld](mailto:user1@mysystems.tld)” an. E-Mails an “[alias@mysystems.tld](mailto:alias@mysystems.tld)” werden dann an die Mailbox dieses Users zugestellt.

Als Zieladressen können auch E-Mail-Konten auf fremden Servern angegeben werden. Postfix leitet diese E-Mails dann weiter. Dabei kann es allerdings zu Problemen mit SPF-Records kommen – schließlich schickt Postfix unter bestimmten Umständen E-Mails unter fremden Domains, für die er laut SPF-Record nicht zuständig ist. SRS (Sender Rewriting Scheme) ist eine Lösung für dieses Problem. Von Erweiterungen, die schwerwiegende Design-Fehler einer Technik wie SPF korrigieren, halte ich allerdings nicht besonders viel, sodass ich euch empfehle, den SPF-Record (wie oben) auf einem “?all” gestellt zu lassen und auf Weiterleitungen zu fremden Servern möglichst zu verzichten. Aliase von lokalen Adressen auf andere lokale Adressen sind kein Problem.

Wenn ein **E-Mail-Verteiler** eingerichtet werden soll, werden mehrere Datensätze mit derselben Quelladresse eingerichtet, also z.B. so:

```
team@domain.tld => user1@domain.tld
team@domain.tld => user2@domain.tld
team@domain.tld => user3@domain.tld
```

Ein **Catch-All** hingegen kann erreicht werden, indem der `source_username` auf `null` gesetzt wird, z.B. so:

```
insert into aliases (source_username, source_domain, destination_username, destination_domain, enabled) values (null, 'domain1.tld', 'catchall', 'mysystems.tld', true);
```

Ein Catch-All kann mit anderen Aliasen auf derselben Domain ko-existieren und “fängt” alle Benutzernamen auf der jeweiligen Domain auf, für die noch kein Alias gesetzt wurde. So kann man Mails zentral aufsammeln, welche an Mailboxen verschickt wurden, die auf dem Mailserver nicht existieren. Beachtet, dass dadurch das Spamaufkommen ggf. höher ist.

### Neue TLS-Policy anlegen (optional)

Mithilfe der TLS Policy-Tabelle kann festgelegt werden, mit welchen Sicherheitsfeatures mit den Mailservern einer bestimmten Domain kommuniziert werden soll. Wenn für die Domain “thomas-leister.de” beispielsweise “dane-only” in “policy” festgelegt wird, wird die Verbindung zu Mailservern dieser Domain nur noch gültig sein, wenn sie DANE-authentifiziert und verschlüsselt ist. Mögliche Policies sind:

-   `none`: Keine Verschlüsselung nutzen, auch wenn der andere Mailserver das unterstützt.
-   `may`: Verschlüsseln, wenn der andere Server dies unterstützt, aber keine Zertifikatsprüfung (self-signed Zertifikate werden akzeptiert).
-   `encrypt`: Zwingend Verschlüsseln, allerdings keine Zertifikatsprüfung (self-signed Zertifikate werden akzeptiert).
-   `dane`: Wenn gültige TLSA-Records gefunden werden, wird zwingend verschlüsselt und das Zertifikat mittels DANE verifiziert. Falls ungültige TLSA-Records gefunden werden, wird auf “encrypt” zurückgegriffen. Falls gar keine TLSA-Records gefunden werden, wird “may” genutzt.
-   `dane-only`: Nur verschlüsselte Verbindungen. Gültige TLSA-Records für den Hostnamen müssen existieren (DANE)
-   `verify`: Nur verschlüsselte Verbindungen + Prüfung der CA. Der Hostname aus dem MX DNS-Record muss im Zertifikat enthalten sein. (Basiert auf Vertrauen in korrekte DNS-Daten)
-   `secure`: Nur verschlüsselte Verbindungen + Prüfung der CA. Der andere Mailserver muss (standardmäßig) einen Hostnamen haben, der “.domain.tld” oder nur “domain.tld” entspricht. Dieser Hostname muss im Zertifikat enthalten sein. Auf das DNS wird nicht zurückgegriffen (Sicherheitsvorteil gegenüber “verify). Beispiel: Eine E-Mail an [user@web.de](mailto:user@web.de) soll gesendet werden. Der MX-Mailserver von Web.de dürfte dann nur den Hostnamen “web.de” oder eine Subdomain davon als Hostnamen haben, z.B. mx.web.de. Eine Verbindung zu mx.web.net wäre nicht zulässig.

Für Domains der großen Anbieter wie gmx.de, web.de und der Telekom kann man “secure” wählen. Bei Posteo und Mailbox.org sogar “dane-only”. Für alle Provider, die keine gültigen TLS-Zertifikate einsetzen, kann “encrypt” gewählt werden. Standardeinstellung für alle anderen Mailserver ist “dane” (siehe main.cf der Postfix Config).

Das Feld “params” wird mit zusätzlichen Infos gefüllt, wenn sie für einen Policy-Typ erforderlich sind, z.B. für einen “secure” Eintrag zu GMX:

```
insert into tlspolicies (domain, policy, params) values ('gmx.de', 'secure', 'match=.gmx.net');
```

Standardmäßig überprüft Postfix bei “secure” – wie oben bereits erwähnt – ob die Empfängerdomain (gmx.de) im Zertifikat des Zielservers vorhanden ist. Bei GMX (und vielen anderen großen Anbietern) ist das allerdings nicht der Fall: Die Mailserver-Zertifikate von GMX sind nur für gmx.net + Subdomains gültig. Ließe man den Datenbank-Eintrag für GMX ohne weitere Einstellungen auf “secure” stehen, könnten an GMX keine Mails mehr übermittelt werden. Deshalb ist es wichtig, für GMX festzulegen, dass im Zertifikat nicht nach “gmx.de” sondern nach “gmx.net” gesucht werden soll. Das können wir mithilfe des Felds “params” und der “match=…” Zeichenkette tun. Wenn nach mehreren Domains gesucht werden soll, können auch mehrere angegeben werden, z.B. so: “match=.gmx.net:.gmx.ch”. Die zusätzlichen Angaben in “params” sind allerdings nicht für jeden Mailprovider notwendig. GMX ist eine Ausnahme – genauso wie z.B. Yahoo. Ob ihr in “params” einen “match”-String angeben müsst, könnt ihr z.B. über [https://de.ssl-tools.net/](https://de.ssl-tools.net/) herausfinden. Wenn die 2-nd-Level-Domain des Mailservers von der Domain der Mailadressen abweicht, muss ein passender match-String angegeben werden.

Andere Einstellungen wie “dane-only” erfordern keine zusätzlichen Angaben in “params”:

```
insert into tlspolicies (domain, policy) values ('mailbox.org', 'dane-only');
```

In diesem Fall wird mit den Mailservern von mailbox.org nur noch DANE-gesichert und verschlüsselt kommuniziert. Die MySQL-Kommandozeile kann mit einem `quit;` wieder verlassen werden.

## Optional: Firewall konfigurieren

Wer vor / auf dem Mailserver eine Firewall betreibt, die den Zugriff auf Ports beschränkt, sollte zuerst alle Mailserver-Ports freischalten:

```
IMAP:           143/tcp
IMAPS:          993/tcp
Submission:     587/tcp
SMTPS:          465/tcp
SMTP:            25/tcp
ManageSieve:   4190/tcp
Web HTTP:        80/tcp
Web HTTPS:      443/tcp
```

**Denkt unbedingt daran, auch eure IPv6-Ports zu öffnen!** - Euer Mailsetup spricht IPv6! :-) Die Ports 143 und 587 können geschlossen bleiben, wenn keine StartTLS-basierenden Verbindung genutzt werden sollen (siehe Hinweis weiter unten).

## Start all the things!

Euer neuer Mailserver ist jetzt fertig konfiguriert. Zeit für einen ersten Start!

```
systemctl start dovecot
systemctl start postfix
```

Wegen des Bugs [#877992](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=877992) startet Postfix nach einem Reboot nicht mehr. Abhilfe schafft folgendes Kommando:

```
systemctl enable postfix@-
```

(beachte das Minuszeichen `-` am Ende!)

Kontrolliert am besten gleich die Logfiles nach auffälligen Fehlern. Ich empfehle das “tail” Tool in einer separaten Terminal-Sitzung. Neue Log-Einträge erscheinen damit sofort auf dem Bildschirm:

```
tail -f /var/log/syslog
```

bzw.

```
tail -f /var/log/mail.log
```

Wenn ihr hier Fehler entdeckt, seht nach, ob ihr alle erforderlichen Änderungen an den Konfigurationsdateien durchgeführt habt (oder ob sich noch beispielhafte Hashes oder Beispieldomains darin befinden).

## Eine Verbindung zum Mailserver herstellen

![Mailserver Logindaten für Thunderbird](https://thomas-leister.de/mailserver-debian-buster/images/thunderbird-login-data.png)

Mailserver Logindaten für Thunderbird

Eine Verbindung könnt ihr über jeden IMAP-fähigen E-Mail-Client und den folgenden Verbindungsparametern herstellen:

-   IMAP(S)
    -   Host: imap.mysystems.tld
    -   Port: 993
    -   Verschlüsselung: TLS
    -   (dieser Server gilt auch für domain2 und domain3, falls vorhanden!)
-   SMTP(S)
    -   Host: smtp.mysystems.tld
    -   Port: 465
    -   Verschlüsselung: TLS
    -   (dieser Server gilt auch für domain2 und domain3, falls vorhanden!)
-   Managesieve (optional, zur Konfiguration der benutzerspezifischen Sieve-Filterregeln)
    -   Host: imap.mysystems.tld
    -   Port: 4190
    -   Verschlüsselung: StartTLS
-   Benutzername: Die **vollständige** E-Mail-Adresse, also @<domain.tld>
-   Passwort: Sollte bekannt sein ;-)

Sollten Verbindungen über die IMAPS (993) und SMTPS (465) Ports nicht möglich sein, kann auch auf die StartTLS-Ports zurückgegriffen werden:

-   IMAP-Server:
    -   Host: mail.mysystems.tld
    -   Port: 143
    -   Verschlüsselung: StartTLS
-   SMTP-Server:
    -   Host: mail.mysystems.tld
    -   Port: 587
    -   Verschlüsselung: StartTLS

Die IETF (Internet Engineering Task Force) empfiehlt seit 2018 allerdings, auf StartTLS Verbindungen zu verzichten, und auf native TLS-Verbindungen zu setzen: [https://tools.ietf.org/html/rfc8314](https://tools.ietf.org/html/rfc8314)

Der erste Login kann ein paar Sekunden in Anspruch nehmen - habt etwas Gedult. Dovecot legt im Hintergrund die Verzeichnisstruktur für den neuen Benutzer an.

## Spamfilter testen

Schickt einfach eine E-Mail mit dem Text

```
XJS*C4JDBQADN1.NSBN3*2IDNEN*GTUBE-STANDARD-ANTI-UBE-TEST-EMAIL*C.34X
```

an einen Account eures neuen Mailservers. Die E-Mail sollte nicht ankommen und im Rspamd-Webinterface erscheint ein entsprechender rot markierter Eintrag in der History.

## Debugging

Sollten Probleme auftreten, hilft ein Blick ins Log!

Das Rspamd Log kannst du z.B. so einsehen und live mitlesen:

```
journalctl -f -u rspamd
```

Postfix so:

```
journalctl -f -u postfix@-.service
```

… und Dovecot so:

```
journalctl -f -u dovecot
```

---