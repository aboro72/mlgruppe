import streamlit as st
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Adresse, Person, Trainer, Kunde, Ansprechpartner, Schiene, \
    Server, FestplattenImage  # Importiere deine SQLAlchemy-Modelle

# Verbindung zur Datenbank herstellen
db_url = "sqlite:///test.db"
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()


# Funktion zum Hinzufügen eines neuen Kunden
def add_kunde():
    st.header("Neuen Kunden hinzufügen")
    kunde_name = st.text_input("Kunde Name")
    kunde_typ = st.selectbox("Kunde Typ", ["Firma", "Behörde"])
    strasse = st.text_input("Straße")
    plz = st.text_input("PLZ")
    stadt = st.text_input("Stadt")
    land = st.text_input("Land")
    ansprechpartner_vorname = st.text_input("Ansprechpartner Vorname")
    ansprechpartner_nachname = st.text_input("Ansprechpartner Nachname")
    ansprechpartner_telefon = st.text_input("Ansprechpartner Telefon")

    if st.button("Kunde speichern"):
        adresse = Adresse(strasse=strasse, plz=plz, stadt=stadt, land=land)
        kunde = Kunde(name=kunde_name, typ=kunde_typ, adresse=adresse)
        ansprechpartner = Ansprechpartner(vorname=ansprechpartner_vorname, nachname=ansprechpartner_nachname,
                                          Telefon=ansprechpartner_telefon)
        kunde.ansprechpartner.append(ansprechpartner)
        session.add(kunde)
        session.commit()
        st.success("Kunde wurde gespeichert!")


# Funktion zum Hinzufügen einer neuen Schiene
def add_schiene():
    st.header("Neue Schiene hinzufügen")
    schiene_name = st.text_input("Schiene Name")
    schiene_status = st.selectbox("Schiene Status", ["Lager", "Unterwegs", "Zurücksetzen", "Imagen"])
    image_name = st.text_input("Image Name")
    image_beschreibung = st.text_area("Image Beschreibung")

    if st.button("Schiene speichern"):
        festplatten_image = FestplattenImage(name=image_name, beschreibung=image_beschreibung)
        schiene = Schiene(name=schiene_name, status=schiene_status, image=festplatten_image)
        session.add(schiene)
        session.commit()
        st.success("Schiene wurde gespeichert!")


# Funktion zum Hinzufügen eines neuen Servers
def add_server():
    st.header("Neuen Server hinzufügen")
    server_name = st.text_input("Server Name")
    server_status = st.selectbox("Server Status", ["Lager", "Unterwegs", "Zurücksetzen", "Unbekannt"])
    image_name = st.text_input("Image Name")
    image_beschreibung = st.text_area("Image Beschreibung")

    if st.button("Server speichern"):
        festplatten_image = FestplattenImage(name=image_name, beschreibung=image_beschreibung)
        server = Server(name=server_name, status=server_status, image=festplatten_image)
        session.add(server)
        session.commit()
        st.success("Server wurde gespeichert!")


def show_pie_charts():
    st.subheader("Kuchendiagramme")

    schiene_status_count = session.query(Schiene.status, Schiene.id).group_by(Schiene.status).count()
    schiene_statuses = session.query(Schiene.status).distinct().all()
    schiene_status_count_dict = {status[0]: session.query(Schiene).filter_by(status=status[0]).count() for status in
                                 schiene_statuses}

    server_status_count = session.query(Server.status, Server.id).group_by(Server.status).count()
    server_statuses = session.query(Server.status).distinct().all()
    server_status_count_dict = {status[0]: session.query(Server).filter_by(status=status[0]).count() for status in
                                server_statuses}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    ax1.pie(schiene_status_count_dict.values(), labels=schiene_status_count_dict.keys(), autopct="%1.1f%%",
            startangle=90)
    ax1.set_title("Schienenstatus")
    ax2.pie(server_status_count_dict.values(), labels=server_status_count_dict.keys(), autopct="%1.1f%%", startangle=90)
    ax2.set_title("Serverstatus")

    st.pyplot(fig)
# Streamlit-Anwendung erstellen
def main():
    st.title("Datenbankanzeige mit Streamlit")

    menu = ["Home", "Datenbank", "Kunde hinzufügen", "Schiene hinzufügen", "Server hinzufügen"]
    choice = st.sidebar.selectbox("Menü", menu)

    if choice == "Home":
        st.subheader("Willkommen zur Datenbankanzeige")

    elif choice == "Datenbank":
        st.subheader("Datenbankverwaltung")
        # Code zur Anzeige von Daten aus der Datenbank

    elif choice == "Kunde hinzufügen":
        add_kunde()

    elif choice == "Schiene hinzufügen":
        add_schiene()

    elif choice == "Server hinzufügen":
        add_server()


if __name__ == "__main__":
    main()
