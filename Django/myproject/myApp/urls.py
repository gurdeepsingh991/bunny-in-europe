from django.urls import path
from .views import create_travel, convert_html_to_word

urlpatterns = [
    path('travel/', convert_html_to_word ),
    path('convert_html_to_word', convert_html_to_word),
]
