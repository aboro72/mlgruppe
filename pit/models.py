from django.db import models
from datetime import timedelta
from kunden.models import Kunde
from trainer.models import Trainer


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
                                                       ('Unbekannt', 'Unbekannt'),
                                                       ('Rückholung', 'Rückholung'),
                                                       ('Weiterleitung', 'Weiterleitung'),
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
                                                       ('Unbekannt', 'Unbekannt'),
                                                       ('Rückholung', 'Rückholung'),
                                                       ('Weiterleitung', 'Weiterleitung'),

                                                       ], default='Zurücksetzen')
    image = models.ForeignKey(FestplattenImageServer, on_delete=models.SET_NULL, null=True, blank=True)
    Bemerkung = models.TextField(max_length=500, default="Fehler/Bemerkung")

    def __str__(self):
        return self.name







