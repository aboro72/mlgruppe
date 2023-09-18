from django.db import models
from pit.models import Server, Schiene
from kurse.models import Kurs
from kunden.models import Kunde
from trainer.models import Trainer


# Create your models here.
class Uebersichts_Tabelle(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    kunde = models.ForeignKey(Kunde, on_delete=models.CASCADE)
    schiene = models.ForeignKey(Schiene, on_delete=models.CASCADE)
    datum = models.DateTimeField(auto_now_add=True)
    beschreibung = models.TextField()

