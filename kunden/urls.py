from django.urls import path, include
from . import views

app_name = "kunde"

urlpatterns = [

    path('create_kunde/', views.create_kunde, name='create_kunde'),

]