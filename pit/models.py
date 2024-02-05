from django.db import models
from datetime import timedelta
from kunden.models import Kunde
from kurse.models import Kurs
from ckeditor.fields import RichTextField


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


class Schiene(models.Model):
    """
    Dieses Modell repräsentiert eine Schiene, die einen Status, einen Druckerfüllstand und ein zugeordnetes Festplatten-Image hat.
    """
    name = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=255, choices=[('Lager', 'Lager'),
                                                       ('Unterwegs', 'Unterwegs'),
                                                       ('Zurücksetzen', 'Zurücksetzen'),
                                                       ('Imagen', 'Imagen'),
                                                       ('Versand', 'Versand'),
                                                       ('Standort', 'Standort'),
                                                       ('Rückholung', 'Rückholung'),
                                                       ('Weiterleitung', 'Weiterleitung'),
                                                       ('Selbstabholung', 'Selbstabholung'),
                                                       ])
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
                                                       ('Versand', 'Versand'),
                                                       ('Standort', 'Standort'),
                                                       ('Rückholung', 'Rückholung'),
                                                       ('Weiterleitung', 'Weiterleitung'),
                                                       ('Selbstabholung', 'Selbstabholung'),

                                                       ], default='Zurücksetzen')
    image = models.ForeignKey(FestplattenImageServer, on_delete=models.SET_NULL, null=True, blank=True)
    Bemerkung = models.TextField(max_length=500, default="Fehler/Bemerkung")

    def __str__(self):
        return self.name


class Abholung(models.Model):
    """
    Dieses Modell repräsentiert eine Selbstabholung/Lieferung
    """
    VA_Nummer = models.IntegerField(max_length=8, unique=True, default='00000')
    Name = models.CharField(max_length=255, null=False, blank=False, default='Mustermann')
    Vorname = models.CharField(max_length=255, null=False, blank=False, default='Max')
    Name2 = models.CharField(max_length=255, null=True, blank=True)
    Vorname2 = models.CharField(max_length=255, null=True, blank=True)
    Mobile1 = models.CharField(max_length=17, null=False, blank=False, default='+49 123 456 7890')
    Mobile2 = models.CharField(max_length=17, null=True, blank=True)
    Email = models.CharField(max_length=255, null=True, blank=True)
    Firmenwagen = models.CharField(max_length=255, choices=[('Ja', 'Ja'),
                                                            ('Privat Fahrzeug', 'Privat Fahrzeug'),
                                                            ('Mietfahrzeug', 'Mietfahrzeug')
                                                            ], null=False, blank=False)
    Fahrzeugvermieter = models.CharField(max_length=255, null=True, blank=True)
    Fahrzeug_Type = models.CharField(max_length=255, null=True, blank=True)
    Kennzeichen = models.CharField(max_length=255, null=False, blank=False, default='K-ML xyz')
    Datum = models.DateField(null=True, blank=True)
    Kunde = models.ForeignKey(Kunde, on_delete=models.CASCADE, null=True, blank=True)
    Schiene = models.ForeignKey(Schiene, on_delete=models.CASCADE, null=True, blank=True)
    Server = models.ForeignKey(Server, on_delete=models.CASCADE, null=True, blank=True)
    Tourdaten = RichTextField(max_length=4900, null=True, blank=True)
    status = models.CharField(max_length=255, choices=[('Rückholung', 'Rückholung'),
                                                       ('Weiterleitung', 'Weiterleitung'),
                                                       ], default='Weiterleitung')


class VersandSchiene(models.Model):
    """
    Dieses Modell repräsentiert einen Versand
    """
    VA_Nummer = models.ForeignKey(Kurs, on_delete=models.CASCADE,)
    Server = models.ForeignKey(Server, on_delete=models.CASCADE, null=True)
    Schiene = models.ForeignKey(Schiene, on_delete=models.CASCADE,)
    Kunde = models.ForeignKey(Kunde, on_delete=models.CASCADE,)