from django.urls import path, include
from . import views

app_name = "pit"

urlpatterns = [
    path('', views.schiene_chart, name='info'),
    path('update_status/<int:item_id>/', views.update_status, name='update_status'),
    path('create_abholung/', views.create_abholung, name='create_abholung'),
    path('abholung_detail/<int:item_id>/', views.abholung_detail, name='abholung_detail'),
    path('update_status_zurueck/<int:item_id>/', views.update_status_zurueck, name='update_status_zurueck'),
    path('update_status_dpd/<int:versand_id>/', views.update_status_dpd, name='update_status_dpd'),
    path('update_status_standort/<int:item_id>/', views.update_status_standort, name='update_status_standort'),
    path('update_status_abholung/<int:item_id>/', views.update_status_abholung, name='update_status_abholung'),
    path('update_status_versand/<int:item_id>/', views.update_status_versand, name='update_status_versand'),
    path('set_versand_status/<int:versand_id>/', views.set_versand_status, name='set_versand_status'),
    path('set_rueckholung_status/<int:versand_id>/', views.set_rueckholung_status, name='set_rueckholung_status'),
]