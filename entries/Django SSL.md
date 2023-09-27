## Sicherung der Django Anwendung mit SSL

[Let’s Encrypt](https://letsencrypt.org/) ist eine kostenlose Zertifizierungsstelle (CA), die SSL-Zertifikate ausstellt. Sie können diese SSL-Zertifikate verwenden, um den Datenverkehr in Ihrer Django-Anwendung zu sichern. Lets Encrypt verfügt über ein automatisches Installationsprogramm namens Certbot. Mit Certbot können Sie Ihrer Website in nur wenigen Minuten ganz einfach ein Zertifikat hinzufügen

Installieren Sie zuerst das Nginx-Paket von Certbot.

```
sudo apt-get update
sudo apt-get install python3-certbot-nginx
```

### [](#configuring-nginx-for-certbot)Konfiguration von Nginx für Certbot

Certbot kann SSL automatisch für Nginx konfigurieren, aber es muss in der Lage sein, das richtige zu finden `server`Blockieren Sie in Ihrer Konfiguration. Es tut dies, indem es nach a sucht `server_name`Direktive, die mit der Domäne übereinstimmt, für die Sie ein Zertifikat anfordern, stellen Sie also sicher, dass Sie die richtige Domäne in der festgelegt haben `/etc/nginx/sites-available/project_name`Datei.

```
. . .
server_name example.com www.example.com;
. . .
```

Falls Sie Änderungen an diesem Serverblock vorgenommen haben, laden Sie Nginx neu.

```
sudo systemctl reload nginx
```

Als nächstes müssen wir konfigurieren `ufw`Firewall, um HTTPS-Datenverkehr zuzulassen.

Also erstmal aktivieren `ufw`Firewall, falls noch nicht geschehen.

```
sudo ufw allow ssh
```

Eintreten `y`Zur Bestätigung fügen Sie als nächstes die folgenden Regeln zur Firewall hinzu.

```
sudo ufw allow 'Nginx Full'
```

Jetzt überprüfen Sie die aktualisierten Regeln mit dem folgenden Befehl.

```
sudo ufw status
```

Dies sollte die Ausgabe sein.

```
Status: active

To                         Action      From
--                         ------      ----
Nginx Full                 ALLOW       Anywhere
22/tcp                     ALLOW       Anywhere
Nginx Full (v6)            ALLOW       Anywhere (v6)
22/tcp (v6)                ALLOW       Anywhere (v6)
```

Jetzt können wir das SSL-Zertifikat mit dem folgenden Befehl erhalten.

```
sudo certbot --nginx -d example.com -d www.example.com
```

Das läuft `certbot`mit dem `--nginx`Plugin, verwenden `-d`um die Domänennamen anzugeben, für die das Zertifikat gültig sein soll.

Für die Einrichtung werden Ihnen eine Reihe von Fragen gestellt.

```
Plugins selected: Authenticator nginx, Installer nginx
Enter email address (used for urgent renewal and security notices) (Enter 'c' to
cancel): admin@djangocentral.com

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Please read the Terms of Service at
https://letsencrypt.org/documents/LE-SA-v1.2-November-15-2017.pdf. You must
agree in order to register with the ACME server at
https://acme-v02.api.letsencrypt.org/directory
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(A)gree/(C)ancel: A

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Would you be willing to share your email address with the Electronic Frontier
Foundation, a founding partner of the Let's Encrypt project and the non-profit
organization that develops Certbot? We'd like to send you email about our work
encrypting the web, EFF news, campaigns, and ways to support digital freedom.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(Y)es/(N)o: Y

Obtaining a new certificate
Performing the following challenges:
http-01 challenge for test.djangocentral.com
Waiting for verification...
Cleaning up challenges
Deploying Certificate to VirtualHost /etc/nginx/sites-enabled/default

Please choose whether or not to redirect HTTP traffic to HTTPS, removing HTTP access.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
1: No redirect - Make no further changes to the webserver configuration.
2: Redirect - Make all requests redirect to secure HTTPS access. Choose this for
new sites, or if you're confident your site works on HTTPS. You can undo this
change by editing your web server's configuration.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Select the appropriate number [1-2] then [enter] (press 'c' to cancel): 2
Redirecting all traffic on port 80 to ssl in /etc/nginx/sites-enabled/default
```

Sobald die Einrichtung abgeschlossen ist, werden diese Konfigurationen aktualisiert und Nginx wird neu geladen, um die neuen Einstellungen zu übernehmen `certbot`wird mit einer Meldung abschließen, die Ihnen mitteilt, dass der Vorgang erfolgreich war und wo Ihre Zertifikate gespeichert sind.

```
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Congratulations! You have successfully enabled https://test.djangocentral.com

You should test your configuration at:
https://www.ssllabs.com/ssltest/analyze.html?d=test.djangocentral.com
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/test.djangocentral.com/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/test.djangocentral.com/privkey.pem
   Your cert will expire on 2020-07-25. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot again
   with the "certonly" option. To non-interactively renew *all* of
   your certificates, run "certbot renew"
 - If you like Certbot, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le
```

Das war's, öffnen Sie Ihren Browser und navigieren Sie zur Domain und Sie sehen eine sichere SSL-Verbindung in Ihrer Django-Anwendung.

### [](#renewing-ssl-certificates)Erneuerung von SSL-Zertifikaten

Die Zertifikate von let's encrypt sind bis zu 90 Tage gültig, nur danach müssen Sie die Zertifikate erneuern. Das Certbot-Paket enthält ein Skript zum Erneuern bestehender Zertifikate. Sie können das Erneuerungsskript mit einem einzigen Probelauf wie unten testen.

```
sudo certbot renew --dry-run
```

Wenn Sie keine Fehler sehen, sind Sie fertig. Bei Bedarf erneuert Certbot Ihre Zertifikate und lädt Nginx neu, um die Änderungen zu übernehmen. Wenn der automatische Verlängerungsprozess jemals fehlschlägt, sendet Let's Encrypt eine Nachricht an die von Ihnen angegebene E-Mail-Adresse und warnt Sie, wenn Ihr Zertifikat bald abläuft.