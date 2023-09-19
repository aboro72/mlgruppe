from django.shortcuts import render
from pit.models import Server, Schiene
from kurse.models import Kurs
from kunden.models import Kunde
from trainer.models import Trainer

# Create your views here.
def index(request):
    return render(request, 'logistik/test.html')