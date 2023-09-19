from django.shortcuts import render, HttpResponse
from kurse.models import Kurs


# Create your views here.

def index(request):
    test = Kurs.objects.all()

    context = {'test': test,
               }
    return render(request, 'logistik/test.html', context)
