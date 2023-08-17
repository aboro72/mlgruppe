from django.urls import path
from . import views

app_name = "orga"

urlpatterns = [
    path('', views.info, name='info'),

]