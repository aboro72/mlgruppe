from django.db import models
from kunden.models import Kunde
from pit.models import Schiene


# Create your models here.
class SchieneBewegung(models.Model):
    """
    Dieses Modell verfolgt die Bewegung einer Schiene, einschließlich des Versanddatums, des Kunden und der Zieladresse.
    """
    schiene = models.ForeignKey(Schiene, on_delete=models.CASCADE)
    datum_versand = models.DateField()
    kunde = models.ForeignKey(Kunde, on_delete=models.CASCADE)
    rueckholung_datum = models.DateField(null=True, blank=True)




    def __str__(self):
        return f"{self.schiene.name} - {self.kunde.name}"
