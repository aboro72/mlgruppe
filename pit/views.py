from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .forms import AbholungForm, VersandForm, ServerForm, SchieneForm
from .models import Schiene, Server, Abholung, Versand, Rueckholung
from datetime import datetime, date, timedelta
from django.contrib.auth.decorators import user_passes_test


def is_pit_group(user):
    return user.groups.filter(name='pit').exists()


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
    versand_liste = Versand.objects.all().order_by('Datum' )
    rueckholung_liste = Rueckholung.objects.all().order_by('RueckDatum')
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
        'versand_liste': versand_liste,
        'rueckholung_liste': rueckholung_liste,
    }

    return render(request, 'pit/schiene_chart.html', context)


@user_passes_test(is_pit_group)
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


@user_passes_test(is_pit_group)
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


@user_passes_test(is_pit_group)
def update_status_versand(request, item_id):
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

    item.status = 'Versand'
    item.save()

    return redirect('pit:info')


@user_passes_test(is_pit_group)
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


@user_passes_test(is_pit_group)
def update_status_abholung(request, item_id):
    """
    Ändert den Status eines Elements auf Abholung"

    ** Views: **
    :views: ´schiene_char´

    ** Return: **
    :return: ´schiene_char´

    """
    try:
        item = Schiene.objects.get(id=item_id)
    except ObjectDoesNotExist:
        try:
            item = Server.objects.get(id=item_id)
        except ObjectDoesNotExist:
            return HttpResponse("Item not found", status=404)

    item.status = 'Selbstabholung'
    item.save()

    return redirect('pit:info')


@user_passes_test(is_pit_group)
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


@user_passes_test(is_pit_group)
def set_rueckholung_status(request, versand_id):
    if request.method == 'POST':
        rückholung = Versand.objects.get(id=versand_id)
        if rückholung.Schiene:
            rückholung.Schiene.status = 'Versand'
            rückholung.Schiene.save()
        if rückholung.Server:
            rückholung.Server.status = 'Versand'
            rückholung.Server.save()

        rückholung.delete()  # Löscht das Versand-Objekt aus der Datenbank
        return redirect('pit:info')  # Setzen Sie hier Ihr gewünschtes Redirect-Ziel


@user_passes_test(is_pit_group)
def update_status_dpd(request, versand_id):
    """
    Ändert den Status der zugehörigen Schiene und Server eines Versandobjekts auf 'Unterwegs'

    ** Views: **
    :views: ´schiene_char´

    ** Return: **
    :return: ´schiene_char´

    """
    if request.method == 'POST':
        try:
            versand = Versand.objects.get(id=versand_id)
            if versand.Schiene:
                versand.Schiene.status = 'Unterwegs'
                versand.Schiene.save()
            if versand.Server:
                versand.Server.status = 'Unterwegs'
                versand.Server.save()
        except Versand.DoesNotExist:
            # Behandeln Sie den Fall, dass das Versand-Objekt nicht gefunden wurde
            pass

    return redirect('pit:info')


@user_passes_test(is_pit_group)
def set_versand_status(request, versand_id):
    if request.method == 'POST':
        versand = Versand.objects.get(id=versand_id)
        if versand.Schiene:
            versand.Schiene.status = 'Versand'
            versand.Schiene.save()
        if versand.Server:
            versand.Server.status = 'Versand'
            versand.Server.save()

        versand.delete()  # Löscht das Versand-Objekt aus der Datenbank
        return redirect('pit:info')  # Setzen Sie hier Ihr gewünschtes Redirect-Ziel


@user_passes_test(is_pit_group)
def create_versand(request):
    if request.method == 'POST':
        form = VersandForm(request.POST)
        if form.is_valid():
            # Erstelle eine Abholungsinstanz, ohne sie zu speichern
            versand = form.save(commit=False)
            # versand.status = 'Unterwegs'  # Setze den Statuswert
            versand.save()  # Speichere die Instanz in der Datenbank
            return redirect('dashboard:index')  # Nach dem Speichern zum Kursliste-View weiterleiten
    else:
        form = VersandForm()

    return render(request, 'pit/create_versand.html', {'form': form})


@user_passes_test(is_pit_group)
def create_server(request):
    if request.method == 'POST':
        form = ServerForm(request.POST)
        if form.is_valid():
            # Erstelle eine Abholungsinstanz, ohne sie zu speichern
            server = form.save(commit=False)
            # versand.status = 'Unterwegs'  # Setze den Statuswert
            server.save()  # Speichere die Instanz in der Datenbank
            return redirect('dashboard:index')  # Nach dem Speichern zum Kursliste-View weiterleiten
    else:
        form = ServerForm()

    return render(request, 'pit/create_server.html', {'form': form})


@user_passes_test(is_pit_group)
def create_schiene(request):
    if request.method == 'POST':
        form = SchieneForm(request.POST)
        if form.is_valid():
            # Erstelle eine Abholungsinstanz, ohne sie zu speichern
            schiene = form.save(commit=False)
            # versand.status = 'Unterwegs'  # Setze den Statuswert
            schiene.save()  # Speichere die Instanz in der Datenbank
            return redirect('dashboard:index')  # Nach dem Speichern zum Kursliste-View weiterleiten
    else:
        form = SchieneForm()

    return render(request, 'pit/create_schiene.html', {'form': form})
