from django.urls import path, include
from . import views

app_name = "pit"

urlpatterns = [
    path('', views.schiene_chart, name='info'),
    path('update_status/<int:item_id>/', views.update_status, name='update_status'),
    path('k-uebersicht/', views.schienen_uebersicht, name='kueb')
]