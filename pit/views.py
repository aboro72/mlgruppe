from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Schiene, Server, SchieneBewegung, Kunde, Kurs
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
    zurücksetzen_count = Schiene.objects.filter(status='Zurücksetzen').count()
    imagen_count = Schiene.objects.filter(status='Imagen').count()
    schienen_lager = Schiene.objects.filter(status='Lager')

    # Server zählen basierend auf ihrem Status
    server_lager_count = Server.objects.filter(status='Lager').count()
    server_unterwegs_count = Server.objects.filter(status='Unterwegs').count()
    server_zurücksetzen_count = Server.objects.filter(status='Zurücksetzen').count()
    server_lager = Server.objects.filter(status='Lager')

    # Sammle Elemente, die zurückgesetzt werden müssen
    items_to_reset = list(Schiene.objects.filter(status='Zurücksetzen')) + list(
        Server.objects.filter(status='Zurücksetzen'))

    # Sammle Schienen, die zurückgeholt werden müssen
    schienen_to_reset = SchieneBewegung.objects.filter(rueckholung_datum__isnull=False).order_by('rueckholung_datum')
    current_week = datetime.now().isocalendar()[1]
    schienen_to_move = SchieneBewegung.objects.filter(rueckholung_datum__week=current_week)
    # Aktualisiere Kontext für das Template
    context = {
        'lager_count': lager_count,
        'unterwegs_count': unterwegs_count,
        'zurücksetzen_count': zurücksetzen_count,
        'imagen_count': imagen_count,
        'server_lager_count': server_lager_count,
        'server_unterwegs_count': server_unterwegs_count,
        'server_zurücksetzen_count': server_zurücksetzen_count,
        'items_to_reset': items_to_reset,
        'schienen_to_reset': schienen_to_reset,
        'schienen_lager': schienen_lager,
        'server_lager': server_lager,
        'schienen_to_move': schienen_to_move,
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

    item.status = 'Zurücksetzen'
    item.save()

    return redirect('pit:info')


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
