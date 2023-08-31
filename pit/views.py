from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Schiene, Server, SchieneBewegung, Kunde
from datetime import datetime


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

    # Server zählen basierend auf ihrem Status
    server_lager_count = Server.objects.filter(status='Lager').count()
    server_unterwegs_count = Server.objects.filter(status='Unterwegs').count()
    server_zurücksetzen_count = Server.objects.filter(status='Zurücksetzen').count()

    # Sammle Elemente, die zurückgesetzt werden müssen
    items_to_reset = list(Schiene.objects.filter(status='Zurücksetzen')) + list(
        Server.objects.filter(status='Zurücksetzen'))

    # Sammle Schienen, die zurückgeholt werden müssen
    schienen_to_reset = SchieneBewegung.objects.filter(rueckholung_datum__isnull=False).order_by('rueckholung_datum')

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
        'schienen_to_reset': schienen_to_reset
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


def schienen_uebersicht(request):
    schienen = Schiene.objects.filter(status='Unterwegs')
    schienen_lager = Schiene.objects.filter(status='Imagen')
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
    schiene_id = request.POST.get('schiene_id')
    dpd_status = request.POST.get('dpd_status') == 'true'

    schiene = Schiene.objects.get(id=schiene_id)
    schiene.dpd_beauftragt = dpd_status
    schiene.save()

    return JsonResponse({'status': 'success'})


