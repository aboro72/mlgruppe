from django.shortcuts import render
from django.http import FileResponse, HttpResponseNotFound
from django.conf import settings
import os
from .forms import ExcelUploadForm
from .utils import generate_passwords_and_save_to_csv, zip_generated_files, cleanup_generated_files
from django.core.files.storage import default_storage


def password_generator_view(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['excel_file']
            file_name = uploaded_file.name  # Erhalt des Dateinamens
            file_path = default_storage.save(os.path.join('generated_files', file_name), uploaded_file)
            full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)  # Vollständiger Pfad

            messages = generate_passwords_and_save_to_csv(full_file_path, file_name)
            return render(request, 'password/passwords_generated.html', {'messages': messages})
    else:
        form = ExcelUploadForm()
    return render(request, 'password/upload_excel.html', {'form': form})


def download_zip(request):
    zip_file_path = zip_generated_files()
    response = FileResponse(open(zip_file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(zip_file_path)}"'

    # Aufrufen der Bereinigungsfunktion, nachdem die Zip-Datei erstellt wurde
    cleanup_generated_files()

    return response


def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_content = request.FILES['file']
            file_name = file_content.name  # Hier den ursprünglichen Dateinamen erhalten

            try:
                generated_file_path, csv_file_paths, messages = generate_passwords_and_save_to_csv(file_content,
                                                                                                   file_name)
                return render(request, 'password/passwords_generated.html', {
                    'zip_file_path': zip_generated_files(),
                    'messages': messages,
                })
            except Exception as e:
                return HttpResponseNotFound(f"Ein Fehler ist aufgetreten: {str(e)}")
    else:
        form = ExcelUploadForm()
    return render(request, 'password/upload_excel.html', {'form': form})
