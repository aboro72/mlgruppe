from django.urls import path
from . import views

app_name = 'kurs'

urlpatterns = [
    # Andere URLs hier ...
    path('create/', views.create_kurs, name='create_kurs'),
    path('kurs_uebersicht/', views.kurs_uebersicht, name='kurs_uebersicht'),
    # path('list/', views.kurs_list, name='kurs_list'),   Annahme, dass du auch eine kurs_list-View hast
]