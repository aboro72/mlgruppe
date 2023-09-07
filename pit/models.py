from django.db import models
from datetime import timedelta







class FestplattenImageNotebook(models.Model):
    """
    Dieses Modell repräsentiert ein Festplatten-Image, das Servern oder Schienen zugeordnet werden kann.
    """
    name = models.CharField(max_length=255, unique=True)
    beschreibung = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class FestplattenImageServer(models.Model):
    """
    Dieses Modell repräsentiert ein Festplatten-Image, das Servern oder Schienen zugeordnet werden kann.
    """
    name = models.CharField(max_length=255, unique=True)
    beschreibung = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class FestplattenImageWorkstation(models.Model):
    """
    Dieses Modell repräsentiert ein Festplatten-Image, das Servern oder Schienen zugeordnet werden kann.
    """
    name = models.CharField(max_length=255, unique=True)
    beschreibung = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Schiene(models.Model):
    """
    Dieses Modell repräsentiert eine Schiene, die einen Status, einen Druckerfüllstand und ein zugeordnetes Festplatten-Image hat.
    """
    name = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=255, choices=[('Lager', 'Lager'),
                                                       ('Unterwegs', 'Unterwegs'),
                                                       ('Zurücksetzen', 'Zurücksetzen'),
                                                       ('Imagen', 'Imagen')])
    DruckerFuellstandA = models.IntegerField(default=100)
    DruckerFuellstandB = models.IntegerField(default=100)
    Nighthawk = models.CharField(max_length=10, default='Beispiel: NH 01')
    datum_kms_aktivierung = models.DateField()
    image = models.ForeignKey(FestplattenImageNotebook, on_delete=models.SET_NULL, null=True)
    Bemerkung = models.TextField(max_length=500, default="Fehler/Bemerkung")

    @property
    def kms_next(self):
        return self.datum_kms_aktivierung + timedelta(days=180)

    def __str__(self):
        return self.name


class Server(models.Model):
    """
    Dieses Modell repräsentiert einen Server und seinen Status
    """
    name = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=255, choices=[('Lager', 'Lager'),
                                                       ('Unterwegs', 'Unterwegs'),
                                                       ('Zurücksetzen', 'Zurücksetzen'),
                                                       ('Unbekannt', 'Unbekannt'),
                                                       ('Rückholung', 'Rückholung'),
                                                       ('Weiterleitung', 'Weiterleitung'),

                                                       ], default='Zurücksetzen')
    image = models.ForeignKey(FestplattenImageServer, on_delete=models.SET_NULL, null=True, blank=True)
    Bemerkung = models.TextField(max_length=500, default="Fehler/Bemerkung")

    def __str__(self):
        return self.name


class SchieneBewegung(models.Model):
    """
    Dieses Modell verfolgt die Bewegung einer Schiene, einschließlich des Versanddatums, des Kunden und der Zieladresse.
    """
    schiene = models.ForeignKey(Schiene, on_delete=models.CASCADE)
    datum_versand = models.DateField()
    kunde = models.ForeignKey(Kunde, on_delete=models.CASCADE)
    rueckholung_datum = models.DateField(null=True, blank=True)
    weiterleitung_datum = models.DateField(null=True, blank=True)
    weiterleitung_kunde = models.ForeignKey(Kunde, related_name='weiterleitung_kundr', null=True, blank=True,
                                            on_delete=models.CASCADE)
    kalenderwoche = models.IntegerField(null=True, blank=True)

    # Neue Felder
    dpd_beauftragt = models.BooleanField(default=False)
    dpd_beauftragt_datum = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.schiene.name} - {self.kunde.name}"


class Kurs(models.Model):
    va_nummer = models.IntegerField(unique=True)  # Eindeutige VA-Nummer
    thema = models.CharField(max_length=50, default='Outlook')
    trainer = models.ForeignKey(Trainer, related_name='kurse', null=True, blank=True,
                                on_delete=models.SET_NULL)  # Ein Trainer kann mehrere Kurse haben
    kunde = models.ForeignKey(Kunde, related_name='kurse', null=True, blank=True,
                              on_delete=models.SET_NULL)  # Ein Kunde kann mehrere Kurse haben
    schiene = models.ForeignKey(Schiene, related_name='kurse', null=True, blank=True,
                                on_delete=models.SET_NULL)  # Eine Schiene kann mehrere Kurse haben
    server = models.ForeignKey(Server, related_name='kurse', null=True, blank=True,
                               on_delete=models.SET_NULL)  # Ein Server kann mehrere Kurse haben
    kurs_start = models.DateTimeField(null=True, blank=True)  # Startzeitpunkt des Kurses
    kurs_ende = models.DateTimeField(null=True, blank=True)  # Endzeitpunkt des Kurses

    def __str__(self):
        return f"{self.va_nummer}"


class Ansprechpartner(models.Model):
    kunde = models.ForeignKey(Kunde, related_name='ansprechpartner', null=True, blank=True,
                              on_delete=models.CASCADE)  # Geändert von Standort zu kunde und aktualisiert related_name
    Anrede = models.CharField(max_length=255, choices=[('Frau', 'Frau'),
                                                       ('Herr', 'Herr'),
                                                       ], default='Herr')
    vorname = models.CharField(max_length=255, null=True, blank=False)
    nachname = models.CharField(max_length=255, null=False, blank=False, default='Müller/Meier/Schmitz')

    Telefon = models.CharField(max_length=17, null=True, blank=True)


