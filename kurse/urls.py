from django.urls import path
from . import views

app_name = 'kurs'

urlpatterns = [
    # Andere URLs hier ...
    path('create/', views.create_kurs, name='create_kurs'),
    # path('list/', views.kurs_list, name='kurs_list'),   Annahme, dass du auch eine kurs_list-View hast
]