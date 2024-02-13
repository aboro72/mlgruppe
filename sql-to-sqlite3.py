import pandas as pd
import sqlite3
import io

# Pfad zur CSV-Datei
csv_file_path = 'c1_ml.csv'

# Pfad zur SQLite-Datenbank
sqlite_db_path = 'db2.sqlite3'


# Analyse der CSV-Datei und Ermittlung der Abschnitte
def analyze_csv(csv_file_path):
    sections = {}
    current_section = []
    current_header = None
    with open(csv_file_path, 'r') as file:
        for line in file:
            if line.startswith('"id"'):  # Annahme: Jeder Abschnitt beginnt mit einer Spalte 'id'
                if current_section:
                    sections[current_header] = ''.join(current_section)
                    current_section = []
                current_header = line.strip()
            current_section.append(line)
        if current_section:  # Den letzten Abschnitt hinzufügen
            sections[current_header] = ''.join(current_section)
    return sections


# Importieren eines Abschnitts in die SQLite-Datenbank
def import_section_to_db(section_data, table_name, conn):
    df = pd.read_csv(io.StringIO(section_data), header=0)
    df.to_sql(table_name, conn, if_exists='replace', index=False)


# Hauptfunktion, die den Importprozess steuert
def import_csv_to_sqlite(csv_file_path, sqlite_db_path):
    sections = analyze_csv(csv_file_path)
    conn = sqlite3.connect(sqlite_db_path)

    # Hier müssen Sie die Zuordnung der Abschnitte zu den Tabellennamen festlegen
    for header, section_data in sections.items():
        table_name = header  # Beispielweise den Header als Tabellennamen verwenden
        import_section_to_db(section_data, table_name, conn)

    conn.close()


# Führen Sie die Hauptfunktion aus
import_csv_to_sqlite(csv_file_path, sqlite_db_path)
