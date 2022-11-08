from django.urls import path
from . import views

urlpatterns = [
    path('words', views.get_words)
]
