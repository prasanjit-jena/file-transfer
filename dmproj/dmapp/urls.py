from django.urls import path
from .views import upload_file, generate_output, download_output_file

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('generate_output/', generate_output, name='generate_output'),
    path('download_output_file/', download_output_file, name='download_output_file'),
]
