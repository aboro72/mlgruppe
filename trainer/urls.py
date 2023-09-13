from django.urls import path
from . import views

app_name = 'trainer'

urlpatterns = [
    # Andere URLs hier ...
    path('create/', views.create_trainer, name='create_trainer'),
    # path('list/', views.kurs_list, name='kurs_list'),   Annahme, dass du auch eine kurs_list-View hast
]