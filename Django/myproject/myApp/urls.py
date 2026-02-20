from django.urls import path
from .views import create_travel

urlpatterns = [
    path('travel/', create_travel),
]