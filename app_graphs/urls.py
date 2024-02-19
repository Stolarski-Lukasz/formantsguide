from django.urls import path
from . import views

urlpatterns = [
    path('create_graphs/', views.create_graphs, name='create_graphs')
]