from django.urls import path, include
from . import views

app_name = "pit"

urlpatterns = [
    path('', views.info, name='info'),

]