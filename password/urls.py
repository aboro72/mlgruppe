from django.urls import path
from .views import password_generator_view, download_zip
from .cleanup_generated_files import cleanup_generated_files
app_name = 'password'

urlpatterns = [
       path('password/', password_generator_view, name='password_generator'),
       path('download-zip/', download_zip, name='download_zip'),
       path('cleanup_generated_files/', cleanup_generated_files, name='cleanup_generated_files'),
]
