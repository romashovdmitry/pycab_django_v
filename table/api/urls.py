from django.urls import path
from . import views

urlpatterns = [
    path('words', views.get_words),
    path('post_new_word', views.post_new_word),
    path('<pk: int  >', views.WordsApiView().as_view())
]
