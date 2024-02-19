from django.urls import path
from . import views

app_name = 'kurs'

urlpatterns = [
    # Andere URLs hier ...
    path('create/', views.create_kurs, name='create_kurs'),
    path('kurs_uebersicht/', views.kurs_uebersicht, name='kurs_uebersicht'),
    path('kurs_details/<int:va_nummer>/', views.kurs_details, name='kurs_details'),
    path('edit_kurs/<int:va_nummer>/', views.edit_kurs, name='edit_kurs'),
    # path('list/', views.kurs_list, name='kurs_list'),   Annahme, dass du auch eine kurs_list-View hast
]