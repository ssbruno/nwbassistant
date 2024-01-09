from django.urls import path
from . import views

urlpatterns = [
    path('nwbassistant/', views.nwbassistant, name='nwbassistant'),
]