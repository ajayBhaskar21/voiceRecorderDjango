from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('convert/', views.convert_audio_to_text, name='convert'),
    
]