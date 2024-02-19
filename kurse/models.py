from django.db import models
from datetime import datetime, timedelta

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
    Hardware_Status = models.CharField(max_length=255, choices=[('Ohne HW', 'Ohne HW'),
                                                                ('mit HW', 'mit HW'),
                                                                ('HW vor Ort', 'HW vor Ort'),
                                                                ('Rückholung', 'Rückholung'),
                                                                ], default='mit HW')

    def __str__(self):
        return f"{self.va_nummer}"

    def save(self, *args, **kwargs):
        super(Kurs, self).save(*args, **kwargs)  # Speichern des Kurs-Objekts

        if self.Hardware_Status == 'mit HW':
            from pit.models import Versand  # Import innerhalb der Methode, um zirkuläre Importe zu vermeiden
            montag_vor_kurs = self.kurs_start - timedelta(days=(self.kurs_start.weekday() + 1) % 7 + 6)
            Versand.objects.create(
                VA_Nummer=self,
                Kunde=self.kunde,
                Datum=montag_vor_kurs
            )

        elif self.Hardware_Status == 'Rückholung':
            from pit.models import Rueckholung
            montag_nach_kurs = self.kurs_ende + timedelta(days=(7 - self.kurs_ende.weekday()) % 7)
            Rueckholung.objects.create(
                VA_Nummer=self,
                Kunde=self.kunde,
                RueckDatum=montag_nach_kurs
            )