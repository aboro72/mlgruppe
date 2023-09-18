from django.db import models


# Create your models here.
class Adresse(models.Model):
    """
    Dieses Modell repräsentiert eine physische Adresse.
    """
    strasse = models.CharField(max_length=255)
    plz = models.CharField(max_length=10)
    stadt = models.CharField(max_length=255)


    def __str__(self):
        return f"{self.strasse}, {self.plz} {self.stadt}"


class Person(models.Model):
    """
    Abstraktes Modell, das gemeinsame Felder für Personen wie Trainer enthält.
    """
    name = models.CharField(max_length=255)
    adresse = models.ForeignKey(Adresse, on_delete=models.CASCADE)
    Telefon = models.CharField(max_length=17, null=True, blank=True)

    class Meta:
        abstract = True
