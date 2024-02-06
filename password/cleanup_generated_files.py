import os
import schedule
import time
from datetime import datetime, timedelta


def cleanup_generated_files():
    directory_path = 'media/generated_files'
    now = datetime.now()

    # Bereinigung des Ordners alle 60 Minuten (1 Stunde)
    schedule.every(60).minutes.do(delete_old_files, directory_path)

    while True:
        schedule.run_pending()
        time.sleep(1)


def delete_old_files(directory_path):
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Fehler beim Löschen von {file_path}: {e}")


if __name__ == "__main__":
    cleanup_generated_files()
