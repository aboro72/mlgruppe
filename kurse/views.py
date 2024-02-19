from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Trainer, Kurs
from .forms import KursForm
from datetime import datetime, timedelta
from collections import defaultdict


def kurs_uebersicht(request):
    kurse = Kurs.objects.all()

    kurs_table = {}
    for kurs in kurse:
        if kurs.kurs_start:
            kunde = str(kurs.kunde)
            kw = f"{kurs.kurs_start.isocalendar()[1]}/{kurs.kurs_start.year}"
            kurs_table.setdefault(kunde, {}).setdefault(kw, []).append(kurs)

    # Filling kurs_details with necessary information for each course
    kurs_details = {kurs.va_nummer: {"thema": kurs.thema,
                                     "trainer": kurs.trainer if kurs.trainer else 'Kein Trainer',
                                     # Hier das korrekte Attribut des Trainers verwenden
                                     "kurs_start": kurs.kurs_start,
                                     "kurs_ende": kurs.kurs_ende,
                                     "Hardware_Status": kurs.Hardware_Status,
                                     "kunde": kurs.kunde}
                    for kurs in kurse}

    calendar_weeks = [f"{week}/{datetime.now().year}" for week in range(1, 53)]

    context = {
        'kurs_table': kurs_table,
        'kurs_details': kurs_details,
        'calendar_weeks': calendar_weeks
    }
    return render(request, 'kurse/kurs_uebersicht.html', context)


def is_orga_group(user):
    return user.groups.filter(name='orga').exists()


# Create your views here.
def create_kurs(request):
    if request.method == 'POST':
        form = KursForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trainer_list')  # Nach dem Speichern zum Kursliste-View weiterleiten
    else:
        form = KursForm()

    return render(request, 'trainer/create_trainer.html', {'form': form})


def kurs_details(request, va_nummer):
    kurs = Kurs.objects.filter(va_nummer=va_nummer).first()
    if kurs:
        data = {
            'va_nummer': kurs.va_nummer,
            'thema': kurs.thema,
            # Weitere Felder, die Sie anzeigen möchten
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Kurs nicht gefunden'}, status=404)


def edit_kurs(request, va_nummer):
    kurs = Kurs.objects.get(va_nummer=va_nummer)
    if request.method == 'POST':
        form = KursForm(request.POST, instance=kurs)
        if form.is_valid():
            form.save()
            # Redirect nach dem Speichern, z.B. zur Kursübersicht
            return redirect('kurs:kurs_uebersicht')
    else:
        form = KursForm(instance=kurs)

    return render(request, 'kurse/edit_kurs.html', {'form': form, 'va_nummer': va_nummer})
