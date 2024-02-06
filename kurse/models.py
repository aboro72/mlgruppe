from django.db import models

from trainer.models import Trainer
from kunden.models import Kunde


# Create your models here.
class Kurs(models.Model):
    va_nummer = models.IntegerField(unique=True)  # Eindeutige VA-Nummer
    thema = models.CharField(max_length=50, default='Outlook')
    trainer = models.ForeignKey(Trainer, related_name='kurse', null=True, blank=True,
                                on_delete=models.SET_NULL)  # Ein Trainer kann mehrere Kurse haben
    kunde = models.ForeignKey(Kunde, related_name='kurse', null=True, blank=True,
                              on_delete=models.SET_NULL)  # Ein Kunde kann mehrere Kurse haben

    kurs_start = models.DateTimeField(null=True, blank=True)  # Startzeitpunkt des Kurses
    kurs_ende = models.DateTimeField(null=True, blank=True)  # Endzeitpunkt des Kurses

    def __str__(self):
        return f"{self.va_nummer} {self.thema} {self.trainer} {self.kunde}"
