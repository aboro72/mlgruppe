from django.urls import path
from . import views

app_name = "codebot"

urlpatterns = [
    path("", views.home, name="home"),
    path("suggest/", views.suggest, name="suggest"),
    path("past/", views.past, name="past"),
    path("delete_past/<Past_id>", views.delete_past, name="delete_past"),
]
