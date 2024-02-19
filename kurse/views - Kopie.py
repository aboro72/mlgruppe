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

    calendar_weeks = [f"{week}/{datetime.now().year}" for week in range(1, 53)]

    context = {
        'kurs_table': kurs_table,
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
