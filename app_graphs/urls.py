from django.urls import path
from . import views

urlpatterns = [
    path('create_spectrogram/', views.create_spectrogram, name='create_spectrogram'),
    path('create_spectrum_slice/', views.create_spectrum_slice, name='create_spectrum_slice')
]