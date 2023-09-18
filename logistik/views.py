from django.shortcuts import render, HttpResponse
from pit.models import Server, Schiene
from kurse.models import Kurs
from kunden.models import Kunde
from trainer.models import Trainer


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the Logistik index.")
