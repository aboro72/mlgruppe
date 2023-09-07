from django.urls import path, include
from . import views

app_name = "pit"

urlpatterns = [
    path('', views.schiene_chart, name='info'),
    path('update_status/<int:item_id>/', views.update_status, name='update_status'),
    path('update_status_zurueck/<int:item_id>/', views.update_status_zurueck, name='update_status_zurueck'),

]