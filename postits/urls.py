from django.urls import path
from . import views


app_name = 'postits'

urlpatterns = [
    path('', views.postit_list, name='postit_list'),
    path('<int:id>/', views.postit_detail, name='postit_detail'),
    path('create/', views.postit_create, name='postit_create'),
    path('update/<int:postit_id>/', views.postit_update, name='postit_update'),
    path('delete/<int:postit_id>/', views.postit_delete, name='postit_delete'),
]