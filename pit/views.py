from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .forms import AbholungForm
from .models import Schiene, Server, Abholung
from datetime import datetime, date, timedelta
from django.db.models import Max


def schiene_chart(request):
    """
    Zähle die Anzahl der Schienen für jeden Status und Server

    ** Models **
    :model:`pit.Schiene`
    :model:`pit.Server`

    ** Template: **
    :template:`pit/schiene_chart.html`

    """
    # Schienen zählen basierend auf ihrem Status
    lager_count = Schiene.objects.filter(status='Lager').count()
    unterwegs_count = Schiene.objects.filter(status='Unterwegs').count()
    unterwegs = Schiene.objects.filter(status='Unterwegs')
    zurücksetzen_count = Schiene.objects.filter(status='Zurücksetzen').count()
    imagen_count = Schiene.objects.filter(status='Imagen').count()
    schienen_lager = Schiene.objects.filter(status='Lager')
    schiene_lager_versand_count = Schiene.objects.filter(status='Versand').count()
    schienen_lager_versand = Schiene.objects.filter(status='Versand')
    schienen_standort_count = Schiene.objects.filter(status='Standort').count()
    schienen_standort = Schiene.objects.filter(status='Standort')
    schienen_weiterleitung_count = Schiene.objects.filter(status='Weiterleitung').count()
    schienen_weiterleitung = Schiene.objects.filter(status='Weiterleitung')
    schienen_zurueck_count = Schiene.objects.filter(status='Rückholung').count()
    schienen_zurueck = Schiene.objects.filter(status='Rückholung')
    schienen_abholung = Schiene.objects.filter(status='Selbstabholung')

    # Server zählen basierend auf ihrem Status
    server_lager_count = Server.objects.filter(status='Lager').count()
    server_unterwegs_count = Server.objects.filter(status='Unterwegs').count()
    server_unterwegs = Server.objects.filter(status='Unterwegs')
    server_zurücksetzen_count = Server.objects.filter(status='Zurücksetzen').count()
    server_lager = Server.objects.filter(status='Lager')
    server_versand_count = Server.objects.filter(status='Versand').count()
    server_versand = Server.objects.filter(status='Versand')
    server_standort_count = Server.objects.filter(status='Standort').count()
    server_standort = Server.objects.filter(status='Standort')
    server_weiterleitung_count = Server.objects.filter(status='Weiterleitung').count()
    server_weiterleitung = Server.objects.filter(status='Weiterleitung')
    server_zurueck_count = Server.objects.filter(status='Rückholung').count()
    server_zurueck = Server.objects.filter(status='Rückholung')
    server_abholung = Server.objects.filter(status='Selbstabholung')

    # Sontiges
    abholung = Abholung.objects.all()

    # Sammle Elemente, die zurückgesetzt werden müssen
    items_to_reset = list(Schiene.objects.filter(status='Zurücksetzen')) + list(
        Server.objects.filter(status='Zurücksetzen'))

    '''
    Sammle Schienen, die zurückgeholt werden müssen wird erstmal nicht mehr gebraucht
    schienen_to_reset = SchieneBewegung.objects.exclude(schiene__status__in=['Lager', 'Zurücksetzen']).filter(
        rueckholung_datum__isnull=False).order_by('rueckholung_datum')
    current_week = datetime.now().isocalendar()[1]
    schienen_to_move = SchieneBewegung.objects.exclude(schiene__status__in=['Lager', 'Zurücksetzen']).filter(
        rueckholung_datum__week=current_week)
    '''
    # Aktualisiere Kontext für das Template
    context = {
        # Schienen
        'lager_count': lager_count,
        'unterwegs_count': unterwegs_count,
        'zurücksetzen_count': zurücksetzen_count,
        'imagen_count': imagen_count,
        'schiene_lager_versand_count': schiene_lager_versand_count,
        'schienen_lager_versand': schienen_lager_versand,
        'schienen_standort_count': schienen_standort_count,
        'schienen_standort': schienen_standort,
        'schienen_lager': schienen_lager,
        'unterwegs': unterwegs,
        'schienen_weiterleitung_count': schienen_weiterleitung_count,
        'schienen_weiterleitung': schienen_weiterleitung,
        'schienen_zurueck_count': schienen_zurueck_count,
        'schienen_zurueck_': schienen_zurueck,
        'schienen_abholung': schienen_abholung,

        # Server
        'server_lager': server_lager,
        'server_lager_count': server_lager_count,
        'server_unterwegs_count': server_unterwegs_count,
        'server_zurücksetzen_count': server_zurücksetzen_count,
        'server_versand_count': server_versand_count,
        'server_standort_count': server_standort_count,
        'server_versand': server_versand,
        'server_standort': server_standort,
        'server_unterwegs': server_unterwegs,
        'server_weiterleitung_count': server_weiterleitung_count,
        'server_weiterleitung': server_weiterleitung,
        'server_zurueck_count': server_zurueck_count,
        'server_zurueck': server_zurueck,
        'server_abholung': server_abholung,

        # sonstiges
        'items_to_reset': items_to_reset,
        'abholung': abholung,

    }

    return render(request, 'pit/schiene_chart.html', context)


def update_status(request, item_id):
    """
    Ändert den Status eines Elements auf "Lager"

    ** Views: **
    :views: ´schiene_char´

    ** Return: **
    :return: ´schiene_char´

    """
    try:
        item = Schiene.objects.get(pk=item_id)
    except ObjectDoesNotExist:
        try:
            item = Server.objects.get(pk=item_id)
        except ObjectDoesNotExist:
            return HttpResponse("Item not found", status=404)

    item.status = 'Lager'
    item.save()

    return redirect('pit:info')


def update_status_zurueck(request, item_id):
    """
    Ändert den Status eines Elements auf Zurücksetzen"

    ** Views: **
    :views: ´schiene_char´

    ** Return: **
    :return: ´schiene_char´

    """
    try:
        item = Schiene.objects.get(pk=item_id)
    except ObjectDoesNotExist:
        try:
            item = Server.objects.get(pk=item_id)
        except ObjectDoesNotExist:
            return HttpResponse("Item not found", status=404)

    item.status = 'Zurücksetzen'
    item.save()

    return redirect('pit:info')


def update_status_dpd(request, item_id):
    """
    Ändert den Status eines Elements auf Unterwegs"

    ** Views: **
    :views: ´schiene_char´

    ** Return: **
    :return: ´schiene_char´

    """
    try:
        item = Schiene.objects.get(pk=item_id)
    except ObjectDoesNotExist:
        try:
            item = Server.objects.get(pk=item_id)
        except ObjectDoesNotExist:
            return HttpResponse("Item not found", status=404)

    item.status = 'Unterwegs'
    item.save()

    return redirect('pit:info')


def update_status_standort(request, item_id):
    """
    Ändert den Status eines Elements auf Zurücksetzen"

    ** Views: **
    :views: ´schiene_char´

    ** Return: **
    :return: ´schiene_char´

    """
    try:
        item = Schiene.objects.get(pk=item_id)
    except ObjectDoesNotExist:
        try:
            item = Server.objects.get(pk=item_id)
        except ObjectDoesNotExist:
            return HttpResponse("Item not found", status=404)

    item.status = 'Standort'
    item.save()

    return redirect('pit:info')


def update_status_abholung(request, item_id):
    """
    Ändert den Status eines Elements auf Abholung"

    ** Views: **
    :views: ´schiene_char´

    ** Return: **
    :return: ´schiene_char´

    """
    try:
        item = Schiene.objects.get(pk=item_id)
    except ObjectDoesNotExist:
        try:
            item = Server.objects.get(pk=item_id)
        except ObjectDoesNotExist:
            return HttpResponse("Item not found", status=404)

    item.status = 'Selbstabholung'
    item.save()

    return redirect('pit:info')


def create_abholung(request):
    if request.method == 'POST':
        form = AbholungForm(request.POST)
        if form.is_valid():
            # Erstelle eine Abholungsinstanz, ohne sie zu speichern
            abholung = form.save(commit=False)
            abholung.status = 'Unterwegs'  # Setze den Statuswert
            abholung.save()  # Speichere die Instanz in der Datenbank
            return redirect('pit:info')  # Nach dem Speichern zum Kursliste-View weiterleiten
    else:
        form = AbholungForm()

    return render(request, 'pit/create_abholung.html', {'form': form})


def abholung_detail(request, item_id):
    abholung = get_object_or_404(Abholung, pk=item_id)
    return render(request, 'pit/abholung_detail.html', {'abholung': abholung})


'''
def schienen_uebersicht(request):
    """
    Zeigt eine Übersicht aller Schienen an.

    ** Models **
    :model:`pit.Schiene`
    :model:`pit.Kunde`

    ** Template: **
    :template:`pit/schienen_uebersicht.html`
    """
    schienen = Schiene.objects.filter(status='Unterwegs')
    schienen_lager = Schiene.objects.filter(status='Lager')
    schienen_infos = []
    kunden = Kunde.objects.all()
    server_lager = Server.objects.filter(status='Lager')

    for schiene in schienen:
        bewegungen = SchieneBewegung.objects.filter(schiene=schiene).order_by('datum_versand')
        letzte_bewegung = bewegungen.last() if bewegungen.exists() else None

        if letzte_bewegung:
            aktueller_status = letzte_bewegung.kunde.name
            naechster_schritt = "Zurückholen" if letzte_bewegung.rueckholung_datum else "Weiterleiten"
            naechstes_datum = letzte_bewegung.rueckholung_datum or letzte_bewegung.weiterleitung_datum
        else:
            aktueller_status = schiene.get_status_display()
            naechster_schritt = "Weiterleiten"
            naechstes_datum = None  # Änderung hier

        schienen_infos.append({
            'schiene': schiene,
            'aktueller_status': aktueller_status,
            'naechster_schritt': naechster_schritt,
            'naechstes_datum': naechstes_datum or datetime.min.date(),
        })

    # Sortieren der Liste nach Datum
    schienen_infos.sort(key=lambda x: x['naechstes_datum'] or datetime.min.date())

    context = {
        'schienen_infos': schienen_infos,
        'kunden': kunden,
        'schienen_lager': schienen_lager,
        'server_lager': server_lager,
    }
    print(schienen_lager.count())
    return render(request, 'pit/schienen_uebersicht.html', context)


def schiene_zurueck(request, schiene_id):
    """
    Setzt den Status einer Schiene auf 'Imagen' zurück.

    ** Arguments: **
    :param schiene_id: ID der Schiene

    ** Return: **
    :return: JSON response
    """
    try:
        bewegung = SchieneBewegung.objects.get(schiene__id=schiene_id)
        schiene = bewegung.schiene
        bewegung.delete()
        schiene.status = 'Imagen'
        schiene.save()
        return JsonResponse({'status': 'success', 'message': 'Schiene zurückgeholt und auf Imagen gesetzt.'})
    except SchieneBewegung.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Schiene nicht gefunden.'})


@csrf_exempt  # Nur für dieses Beispiel. Stellen Sie sicher, dass CSRF-Token in der Produktion korrekt behandelt werden.
def schiene_weiterleiten(request):
    """
    Leitet eine Schiene an einen Kunden weiter.

    ** Method: **
    :method: POST

    ** Return: **
    :return: JSON response
    """
    if request.method == 'POST':
        try:
            schiene_id = request.POST.get('schiene_id')
            kunde_id = request.POST.get('kunde')  # Annahme, dass der Kunde als ID übertragen wird
            weiterleitungs_datum_str = request.POST.get('weiterleitungs_datum')
            rueckholungs_datum_str = request.POST.get('rueckholungs_datum')

            # Datum in ein Python datetime-Objekt umwandeln
            weiterleitungs_datum = datetime.strptime(weiterleitungs_datum_str, '%Y-%m-%d').date()
            rueckholungs_datum = datetime.strptime(rueckholungs_datum_str, '%Y-%m-%d').date()

            # Schiene und Kunde aus der Datenbank holen
            schiene = Schiene.objects.get(id=schiene_id)
            kunde = Kunde.objects.get(id=kunde_id)  # Ändern Sie dies entsprechend Ihrem Kunde-Modell

            # Erstellen Sie ein neues SchieneBewegung-Objekt
            neue_bewegung = SchieneBewegung(
                schiene=schiene,
                datum_versand=weiterleitungs_datum,
                kunde=kunde,
                weiterleitung_datum=weiterleitungs_datum,
                rueckholung_datum=rueckholungs_datum,
                # Weitere Felder können hier eingefügt werden
            )
            neue_bewegung.save()

            return JsonResponse({'status': 'success', 'message': 'Schiene erfolgreich weitergeleitet.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Ungültige Anfrage'})


@csrf_exempt  # Überspringen Sie die CSRF-Überprüfung für dieses Beispiel
def update_dpd_status(request):
    """
    Aktualisiert den DPD-Status einer Schiene.

    ** Method: **
    :method: POST

    ** Return: **
    :return: JSON response
    """
    schiene_id = request.POST.get('schiene_id')
    dpd_status = request.POST.get('dpd_status') == 'true'

    schiene = Schiene.objects.get(id=schiene_id)
    schiene.dpd_beauftragt = dpd_status
    schiene.save()

    return JsonResponse({'status': 'success'})


def course_table(request):
    """
    Zeigt eine Tabelle mit Informationen zu Kursen an.

    ** Models: **
    :model:`pit.Schiene`

    ** Template: **
    :template:`pit/course_table.html`
    """
    schienen = Schiene.objects.all()  # Holen Sie sich alle Schienen, die Sie anzeigen möchten
    today = date.today()
    start_of_year = date(today.year, 1, 1)
    end_of_year = date(today.year, 12, 31)

    calendar_weeks = []
    current_date = start_of_year
    while current_date <= end_of_year:
        calendar_weeks.append(current_date.strftime("%V"))
        current_date += timedelta(weeks=1)

    schienen_info = []  # Liste für gesammelte Informationen erstellen
    for schiene in schienen:
        kunde = get_current_kunde(schiene, today)
        schienen_info.append((schiene, kunde))  # Schiene und Kunde als Tupel hinzufügen

    context = {
        'schienen_info': schienen_info,  # Fügen Sie die Liste in den Kontext ein
        'calendar_weeks': calendar_weeks
    }
    return render(request, 'pit/course_table.html', context)


def get_current_kunde(schiene, current_date):
    """
    Gibt den aktuellen Kunden für eine bestimmte Schiene zurück.

    ** Arguments: **
    :param schiene: Schiene-Objekt
    :param current_date: Aktuelles Datum

    ** Return: **
    :return: Kunde-Objekt oder None
    """
    bewegungen = SchieneBewegung.objects.filter(schiene=schiene, datum_versand__lte=current_date).order_by(
        '-datum_versand')
    if bewegungen.exists():
        return bewegungen.first().kunde
    return None


@csrf_exempt
def set_rueckholung_status(request):
    """
    Setzt den Rückholstatus einer Schiene.

    ** Method: **
    :method: POST

    ** Return: **
    :return: JSON response
    """
    schiene_id = request.POST.get('schiene_id')
    try:
        schiene = Schiene.objects.get(id=schiene_id)
        schiene.status = 'Rückholung'
        schiene.save()
        return JsonResponse({'status': 'success'})
    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Schiene nicht gefunden.'})


@csrf_exempt
def schiene_weiterleiten_neu(request):
    """
    Leitet eine Schiene an einen neuen Kunden weiter.

    ** Method: **
    :method: POST

    ** Return: **
    :return: JSON response
    """
    if request.method == 'POST':
        schiene_id = request.POST.get('schiene_id')
        kunde_id = request.POST.get('kunde_id')
        datum_versand = datetime.now().date()  # Aktuelles Datum
        next_rueckholung_datum = datum_versand + timedelta(days=30)  # Beispielsdatum für die nächste Rückholung

        try:
            schiene = Schiene.objects.get(id=schiene_id)
            kunde = Kunde.objects.get(id=kunde_id)

            neue_bewegung = SchieneBewegung(
                schiene=schiene,
                kunde=kunde,
                datum_versand=datum_versand,
                rueckholung_datum=next_rueckholung_datum,
            )
            neue_bewegung.save()

            schiene.status = 'Unterwegs'  # Status ändern, wenn die Schiene weitergeleitet wird
            schiene.save()

            return JsonResponse({'status': 'success'})

        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Schiene oder Kunde nicht gefunden.'})


@csrf_exempt
def weiterleitung_schiene(request):
    if request.method == 'POST':
        schiene_id = request.POST.get('schiene_id')
        kunde_id = request.POST.get('kunde_id')
        datum_versand = request.POST.get('datum_versand')
        rueckholung_datum = request.POST.get('rueckholung_datum')

        try:
            schiene = Schiene.objects.get(id=schiene_id)
            kunde = Kunde.objects.get(id=kunde_id)

            neue_bewegung = SchieneBewegung(
                schiene=schiene,
                kunde=kunde,
                datum_versand=datum_versand,
                rueckholung_datum=rueckholung_datum
            )
            neue_bewegung.save()

            return JsonResponse({'status': 'success'})

        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Schiene oder Kunde nicht gefunden.'})

'''
