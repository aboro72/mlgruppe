from django.db import models
from trainer.models import Adresse


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
