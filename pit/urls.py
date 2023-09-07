from django.urls import path, include
from . import views

app_name = "pit"

urlpatterns = [
    path('', views.schiene_chart, name='info'),
    path('update_status/<int:item_id>/', views.update_status, name='update_status'),
    path('update_status_zurueck/<int:item_id>/', views.update_status_zurueck, name='update_status_zurueck'),
    path('k-uebersicht/', views.schienen_uebersicht, name='kueb'),
    path('course_table/', views.course_table, name='course_table'),
    path('schiene_weiterleiten/', views.schiene_weiterleiten_neu, name='schiene_weiterleiten'),
]