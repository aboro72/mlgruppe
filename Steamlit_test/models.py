from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from datetime import timedelta

Base = declarative_base()


class Adresse(Base):
    __tablename__ = 'adresse'

    id = Column(Integer, primary_key=True)
    strasse = Column(String(255))
    plz = Column(String(10))
    stadt = Column(String(255))
    land = Column(String(255))

    def __str__(self):
        return f"{self.strasse}, {self.plz} {self.stadt}, {self.land}"


class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    adresse_id = Column(Integer, ForeignKey('adresse.id'))
    adresse = relationship("Adresse")
    Telefon = Column(String(17))

    def __str__(self):
        return self.name


class Trainer(Person):
    __tablename__ = 'trainer'

    id = Column(Integer, ForeignKey('person.id'), primary_key=True)


class Kunde(Base):
    __tablename__ = 'kunde'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    typ = Column(String(255))
    adresse_id = Column(Integer, ForeignKey('adresse.id'))
    adresse = relationship("Adresse")

    def __str__(self):
        return f"{self.name} ({self.typ})"


class FestplattenImage(Base):
    __tablename__ = 'festplatten_image'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    beschreibung = Column(Text)

    def __str__(self):
        return self.name


class Schiene(Base):
    __tablename__ = 'schiene'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    status = Column(String(255))
    DruckerFuellstandA = Column(Integer, default=100)
    DruckerFuellstandB = Column(Integer, default=100)
    Nighthawk = Column(String(10), default='Beispiel: NH 01')
    datum_kms_aktivierung = Column(DateTime)
    image_id = Column(Integer, ForeignKey('festplatten_image.id'))
    image = relationship("FestplattenImage")
    Bemerkung = Column(Text, default="Fehler/Bemerkung")

    @property
    def kms_next(self):
        return self.datum_kms_aktivierung + timedelta(days=180)

    def __str__(self):
        return self.name


class Server(Base):
    __tablename__ = 'server'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    status = Column(String(255))
    Bemerkung = Column(Text, default="Fehler/Bemerkung")

    def __str__(self):
        return self.name


class SchieneBewegung(Base):
    __tablename__ = 'schiene_bewegung'

    id = Column(Integer, primary_key=True)
    schiene_id = Column(Integer, ForeignKey('schiene.id'))
    schiene = relationship("Schiene")

    kunde_id = Column(Integer, ForeignKey('kunde.id'))
    kunde = relationship("Kunde", foreign_keys=[kunde_id])  # foreign_keys hinzugefügt

    datum_versand = Column(DateTime)
    rueckholung_datum = Column(DateTime)
    weiterleitung_datum = Column(DateTime)
    weiterleitung_kunde_id = Column(Integer, ForeignKey('kunde.id'))
    weiterleitung_kunde = relationship("Kunde", foreign_keys=[weiterleitung_kunde_id])  # foreign_keys hinzugefügt

    dpd_beauftragt = Column(Boolean, default=False)
    dpd_beauftragt_datum = Column(DateTime)

    def __str__(self):
        return f"{self.schiene.name} - {self.kunde.name}"


class Kurs(Base):
    __tablename__ = 'kurs'

    id = Column(Integer, primary_key=True)
    va_nummer = Column(Integer, unique=True)
    thema = Column(String(50), default='Outlook')
    trainer_id = Column(Integer, ForeignKey('trainer.id'))
    trainer = relationship("Trainer")
    kunde_id = Column(Integer, ForeignKey('kunde.id'))
    kunde = relationship("Kunde")
    schiene_id = Column(Integer, ForeignKey('schiene.id'))
    schiene = relationship("Schiene")
    server_id = Column(Integer, ForeignKey('server.id'))
    server = relationship("Server")
    kurs_start = Column(DateTime)
    kurs_ende = Column(DateTime)

    def __str__(self):
        return f"{self.va_nummer}"


class Ansprechpartner(Base):
    __tablename__ = 'ansprechpartner'

    id = Column(Integer, primary_key=True)
    kunde_id = Column(Integer, ForeignKey('kunde.id'))
    kunde = relationship("Kunde")
    Anrede = Column(String(255))
    vorname = Column(String(255))
    nachname = Column(String(255), default='Müller/Meier/Schmitz')
    Telefon = Column(String(17))


# Erstelle eine SQLite-Datenbank und führe die Erstellung der Tabellen durch
engine = create_engine('sqlite:///test.db')
Base.metadata.create_all(engine)

