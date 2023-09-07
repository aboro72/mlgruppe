from django.db import models
from start.models import Adresse


# Create your models here.

class Kunde(models.Model):
    """
    Dieses Modell repräsentiert einen Kunden, der entweder eine Firma oder eine Behörde sein kann.
    """
    name = models.CharField(max_length=255)
    typ = models.CharField(max_length=255, choices=[('Firma', 'Firma'), ('Behörde', 'Behörde')])
    adresse = models.ForeignKey(Adresse, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.typ})"


class Ansprechpartner(models.Model):
    kunde = models.ForeignKey(Kunde, related_name='ansprechpartner', null=True, blank=True,
                              on_delete=models.CASCADE)  # Geändert von Standort zu kunde und aktualisiert related_name
    Anrede = models.CharField(max_length=255, choices=[('Frau', 'Frau'),
                                                       ('Herr', 'Herr'),
                                                       ], default='Herr')
    vorname = models.CharField(max_length=255, null=True, blank=False)
    nachname = models.CharField(max_length=255, null=False, blank=False, default='Müller/Meier/Schmitz')

    Telefon = models.CharField(max_length=17, null=True, blank=True)
