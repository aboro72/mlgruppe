from django.shortcuts import render, redirect, get_object_or_404
from .models import Kunde

from .forms import KundeForm


# Create your views here.
def create_kunde(request):
    if request.method == 'POST':
        form = KundeForm(request.POST)
        if form.is_valid():
            # Erstelle eine Abholungsinstanz, ohne sie zu speichern
            # Versand = form.save(commit=False)
            # versand.status = 'Unterwegs'  # Setze den Statuswert
            Kunde.save()  # Speichere die Instanz in der Datenbank
            return redirect('pit:info')  # Nach dem Speichern zum Kursliste-View weiterleiten
    else:
        form = KundeForm()

    return render(request, 'kunden/create_kunde.html', {'form': form})
