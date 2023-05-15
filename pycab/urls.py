from django.contrib import admin
from django.urls import path, include, re_path

from users.views import Registration, Login, InfoPage, logout, \
    password_step_first, password_step_second, password_step_lust
from table.views.words import table, delete_word, modify_word
from table.views.get_message import get_message

urlpatterns = [
    # registrations pages
    path('', Registration.as_view(), name='reg'),
    path('login', Login.as_view(), name='login'),
    path('infopage', InfoPage.as_view(), name='infopage'),
    path('logout', logout, name='logout'),

    # working with words pages
    path('table', table, name='table'),
    path('delete_word/<pk>', delete_word, name='delete'),
    path('modify/<pk>', modify_word, name='modify'),

    # recreating password pages
    path('newpassword_step_first', password_step_first,
         name='password_step_first'),
    path('password_step_second', password_step_second,
         name='password_step_second'),
    path('password_step_lust', password_step_lust,
         name='password_step_lust'),

    # api url
    path('api/', include('table.api.urls')),

    # for Telegram webhook url
    path('telegram', get_message),

    # for incorrect URLs
    re_path(r"\S+/$", Registration.as_view(), name="registerPage")

]
