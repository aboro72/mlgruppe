from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
def info(request):
    return HttpResponse("Ich bin ein Platzhalter der Start seite.")
