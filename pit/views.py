from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from .models import Schiene, Server, SchieneBewegung


def schiene_chart(request):
    """
    Zähle die Anzahl der Schienen für jeden Status

    ** Models **
    ``model``
    :model:`pit.Schiene`
    :model:`pit.Server`

    **Template:**

    :template:`pit/schiene_chart.html`


    """
    lager_count = Schiene.objects.filter(status='Lager').count()
    unterwegs_count = Schiene.objects.filter(status='Unterwegs').count()
    zurücksetzen_count = Schiene.objects.filter(status='Zurücksetzen').count()
    imagen_count = Schiene.objects.filter(status='Imagen').count()

    server_lager_count = Server.objects.filter(status='Lager').count()
    server_unterwegs_count = Server.objects.filter(status='Unterwegs').count()
    server_zurücksetzen_count = Server.objects.filter(status='Zurücksetzen').count()

    context = {
        'lager_count': lager_count,
        'unterwegs_count': unterwegs_count,
        'zurücksetzen_count': zurücksetzen_count,
        'imagen_count': imagen_count,
        'server_lager_count': server_lager_count,
        'server_unterwegs_count': server_unterwegs_count,
        'server_zurücksetzen_count': server_zurücksetzen_count
    }

    # Hole die Server und Schienen, die zurückgesetzt werden müssen
    items_to_reset = list(Schiene.objects.filter(status='Zurücksetzen')) + list(
        Server.objects.filter(status='Zurücksetzen'))

    context.update({
        'items_to_reset': items_to_reset
    })

    return render(request, 'pit/schiene_chart.html', context)


def update_status(request, item_id):
    '''
    :views: ´schiene_char´
    :return: ´schiene_char´
    '''
    try:
        item = Schiene.objects.get(pk=item_id)
    except Schiene.DoesNotExist:
        item = Server.objects.get(pk=item_id)

    item.status = 'Lager'
    item.save()

    return redirect('schiene_chart')


def schienen_uebersicht(request):
    schienen = Schiene.objects.all()
    schienen_infos = []

    for schiene in schienen:
        letzte_bewegung = SchieneBewegung.objects.filter(schiene=schiene).order_by('-datum_versand').first()

        if letzte_bewegung:
            aktueller_status = letzte_bewegung.kunde.name
            naechster_schritt = "Zurückholen" if letzte_bewegung.rueckholung_datum else "Weiterleiten"
            naechstes_datum = letzte_bewegung.rueckholung_datum if letzte_bewegung.rueckholung_datum else letzte_bewegung.weiterleitung_datum
        else:
            aktueller_status = schiene.get_status_display()
            naechster_schritt = "Weiterleiten"
            naechstes_datum = schiene.datum_kms_aktivierung

        schienen_infos.append({
            'schiene': schiene,
            'aktueller_status': aktueller_status,
            'naechster_schritt': naechster_schritt,
            'naechstes_datum': naechstes_datum
        })

    context = {
        'schienen_infos': schienen_infos
    }
    return render(request, 'schienen_uebersicht.html', context)
