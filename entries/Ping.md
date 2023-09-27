**Ping-Befehl mit Parameter ausführen:** Geben Sie den Befehl _ping_ in die Kommandozeile ein und übergeben Sie diesem entweder die IP-Adresse oder den Hostnamen des Zielrechners als Parameter, indem Sie die entsprechende Information durch ein Leerzeichen getrennt an den Befehl anhängen.

Ping-Befehl mit der IP-Adresse des Zielrechners:

```mixed
ping 8.8.8.8
```

Ping-Befehl mit Hostname und Domain des Zielrechners:

```mixed
ping google-public-dns-a.google.com
```

[![Der Kommandozeilen-Befehl „ping“](https://www.ionos.de/digitalguide/fileadmin/DigitalGuide/Screenshots_2019/ping-befehl.png "Der Kommandozeilen-Befehl „ping“")](https://www.ionos.de/digitalguide/fileadmin/DigitalGuide/Screenshots_2019/ping-befehl.png)

Als Parameter für den Ping-Befehl verwenden wir die IP-Adresse des von Google bereitgestellten DNS-Servers: 8.8.8.8.

Bestätigen Sie Ihre Eingabe mit einem Enter, um das CMD-Programm mit dem gewählten Parameter auszuführen.

**3. Output des Ping-Befehls:** Wird Ping ohne weitere Optionen ausgeführt, sendet das Programm vier Datenpakete an den angegebenen Zielrechner und gibt Ihnen statistische Informationen zu den Anfragen im Terminal aus.

Die Terminalausgabe umfasst eine Übersichtstabelle, die die jeweilige Antwortzeit, die Paketgröße sowie die TTL pro Antwortpaket aufführt. Darüber hinaus erhalten Sie statistische Informationen zu gesendeten, empfangenen und verlorenen Pakten inklusive dem Paketverlust in Prozent sowie eine Auswertung der minimalen, maximalen und durchschnittlichen Antwortzeit.

[![Ping-Statistik im Windows-Terminal](https://www.ionos.de/digitalguide/fileadmin/DigitalGuide/Screenshots_2019/ping-statistik.png "Ping-Statistik im Windows-Terminal")](https://www.ionos.de/digitalguide/fileadmin/DigitalGuide/Screenshots_2019/ping-statistik.png)

Die Antwortzeit des Google-DNS-Servers beträgt im Durchschnitt 32 ms. Bei einer TTL von 119 ist davon auszugehen, dass jedes Paket 8 Netzwerkknoten passiert hat (127 - 8 = 119).

Eine ähnliche Ausgabe erhalten Sie, wenn Sie den Ping-Test mit dem Hostnamen des Zielrechners durchführen.

In diesem Fall wird der Rechnername gemäß den DNS-Einstellungen Ihres Betriebssystems in die zugehörige IP-Adresse aufgelöst. Die IP-Adresse wird Ihnen im Rahmen der Programmausgabe zusammen mit der Ping-Statistik angezeigt.

[![Ping-Statistik im Windows-Terminal](https://www.ionos.de/digitalguide/fileadmin/DigitalGuide/Screenshots_2019/ping-statistik-2.png "Ping-Statistik im Windows-Terminal")](https://www.ionos.de/digitalguide/fileadmin/DigitalGuide/Screenshots_2019/ping-statistik-2.png)

Im Beispiel wird der Hostname google-public-dns-a.google.com in die IP-Adresse 8.8.8.8 aufgelöst und viermal angepingt.

Ist der adressierte Zielrechner hingegen nicht erreichbar, unterscheidet sich die Terminalausgabe je nachdem, ob Sie das Ziel via IP oder Hostname adressieren.

Ist die von Ihnen angegebene [IP-Adresse](https://www.ionos.de/digitalguide/server/knowhow/was-ist-eine-ip-adresse/ "Was ist eine IP-Adresse?") nicht erreichbar, treffen die erwarteten Antwortpakete nicht in der dafür vorgesehenen Zeitspanne ein. In diesem Fall erhalten Sie die Terminalausgabe: „Zeitüberschreitung der Anforderung“.

[![Fehlgeschlagener Ping-Test](https://www.ionos.de/digitalguide/fileadmin/DigitalGuide/Screenshots_2019/fehlgeschlagener-ping-test.png "Fehlgeschlagener Ping-Test")](https://www.ionos.de/digitalguide/fileadmin/DigitalGuide/Screenshots_2019/fehlgeschlagener-ping-test.png)

Fehlgeschlagener ICMP-Echo-Request an die IP-Adresse 8.8.8.7

Kann der mit dem Ping-Befehl übergebene [Hostname](https://www.ionos.de/digitalguide/hosting/hosting-technik/hostname/ "Hostname") nicht in eine entsprechende IP-Adresse aufgelöst werden, beispielsweise, weil Sie sich vertippt haben, erhalten Sie folgende Fehlermeldung:

[![Fehlgeschlagener Ping-Test](https://www.ionos.de/digitalguide/fileadmin/DigitalGuide/Screenshots_2019/fehlgeschlagener-ping-test-2.png "Fehlgeschlagener Ping-Test")](https://www.ionos.de/digitalguide/fileadmin/DigitalGuide/Screenshots_2019/fehlgeschlagener-ping-test-2.png)

Fehlgeschlagener ICMP-Echo-Request an einen Rechner mit dem Namen gogle-public-dns-a.google.com

## Die Optionen des Ping-Befehls

Bei Bedarf können Sie den Ping-Befehl mit einer Reihe von Optionen ausführen, um die Standardwerte des ICMP-Echo-Requests anzupassen. Die nachfolgende Tabelle gibt Ihnen einen Überblick über die wichtigsten Optionen des Kommandozeilenbefehls.

Option (Auswahl)

Beschreibung

-t

Sofern Sie den Befehl ping mit der Option -t übergeben, wird der adressierte Zielrechner so lange angepingt, bis Sie den Vorgang mit STRG + C beenden, um sich die Ping-Statistik anzeigen zu lassen. Man spricht von einem Dauerping.

-a <ip>

Verwenden Sie den Befehl ping mit der Option -a und der IP-Adresse des Zielrechners, um den Hostnamen des Ziels zu ermitteln. Der Rechnername wird Ihnen zusammen mit der Ping-Statistik im Terminal angezeigt.

-n <anzahl>

Mit der Option -n definieren Sie die gewünschte Anzahl der ICMP-Echo-Requests. In der Standardeinstellung sendet ping 4 Anfragen.

-l <größe>

Mit der Option -l definieren Sie die Größe des ICMP-Echo-Request-Pakets in Byte. Der Standardwert beträgt 32. Mit Ping können Datenpakete mit einer Maximalgröße von 65.527 Byte verschickt werden.

-f

Wird der Befehl ping mit der Option -f ausgeführt, setzt das Programm das „Do not Fragment“-Flag im IP-Header des ICMP-Echo-Request-Pakets auf 1. Eine solche Anfrage kann von Netzwerkknoten auf dem Weg zum Ziel nicht in kleinere Einheiten aufgeteilt werden. Diese Option steht nur in IPv4-Netzwerken zur Verfügung.

-i <TTL>

Mit der Option -i definieren Sie eine benutzerdefinierte TTL für Ihren ICMP-Echo-Request. Das Maximum liegt bei 255.

-4

Die Option -4 erzwingt die Verwendung von IPv4 und kommt nur zum Einsatz, wenn der Empfänger mithilfe des Rechnernamens adressiert wird.

-6

Die Option -6 erzwingt die Verwendung von IPv6 und kommt nur zum Einsatz, wenn der Empfänger mithilfe des Rechnernamens adressiert wird.