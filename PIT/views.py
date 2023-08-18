from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from .models import Schiene, Server


def schiene_chart(request):
    # Zählen Sie die Anzahl der Schienen für jeden Status
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
    try:
        item = Schiene.objects.get(pk=item_id)
    except Schiene.DoesNotExist:
        item = Server.objects.get(pk=item_id)

    item.status = 'Lager'
    item.save()

    return redirect('schiene_chart')
