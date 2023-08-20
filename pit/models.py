from django.db import models
from datetime import timedelta


class Adresse(models.Model):
    """
    Dieses Modell repräsentiert eine physische Adresse.
    """
    strasse = models.CharField(max_length=255)
    plz = models.CharField(max_length=10)
    stadt = models.CharField(max_length=255)
    land = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.strasse}, {self.plz} {self.stadt}, {self.land}"


class Person(models.Model):
    """
    Abstraktes Modell, das gemeinsame Felder für Personen wie Trainer enthält.
    """
    name = models.CharField(max_length=255)
    adresse = models.ForeignKey(Adresse, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Trainer(Person):
    """
    Dieses Modell repräsentiert einen Trainer, der Kurse leitet.
    """


class Kunde(models.Model):
    """
    Dieses Modell repräsentiert einen Kunden, der entweder eine Firma oder eine Behörde sein kann.
    """
    name = models.CharField(max_length=255)
    typ = models.CharField(max_length=255, choices=[('Firma', 'Firma'), ('Behörde', 'Behörde')])
    adresse = models.ForeignKey(Adresse, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.typ})"


class FestplattenImage(models.Model):
    """
    Dieses Modell repräsentiert ein Festplatten-Image, das Servern oder Schienen zugeordnet werden kann.
    """
    name = models.CharField(max_length=255, unique=True)
    beschreibung = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


2


class Kurs(models.Model):
    """
    Dieses Modell repräsentiert einen Kurs, der von einem Trainer geleitet wird und eine eindeutige VA-Nummer hat.
    """
    kurz_art = models.CharField(max_length=255)
    va_nummer = models.CharField(max_length=255, unique=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    kunde = models.ForeignKey(Kunde, on_delete=models.CASCADE, default="Ich bin eine Beispiel Kaserne")

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
    image = models.ForeignKey(FestplattenImage, on_delete=models.SET_NULL, null=True)
    Bemerkung = models.TextField(max_length=500, default="Fehler/Bemerkung")

    @property
    def kms_next(self):
        return self.datum_kms_aktivierung + timedelta(days=180)

    def __str__(self):
        return self.name


2


class Server(models.Model):
    """
    Dieses Modell repräsentiert einen Server und seinen Status
    """
    name = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=255, choices=[('Lager', 'Lager'),
                                                       ('Unterwegs', 'Unterwegs'),
                                                       ('Zurücksetzen', 'Zurücksetzen'),
                                                       ('Unbekannt', 'Unbekannt')
                                                       ], default='Zurücksetzen')
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
    ziel_adresse = models.ForeignKey(Adresse, related_name='ziel_adresse', on_delete=models.CASCADE)
    rueckholung_datum = models.DateField(null=True, blank=True)
    weiterleitung_datum = models.DateField(null=True, blank=True)
    weiterleitung_kunde = models.ForeignKey(Kunde, related_name='weiterleitung_kundr', null=True, blank=True,
                                            on_delete=models.CASCADE)
    weiterleitung_adresse = models.ForeignKey(Adresse, related_name='weiterleitung_adresse', null=True, blank=True,
                                              on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.schiene.name} - {self.kunde.name}"
