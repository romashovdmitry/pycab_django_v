from django.contrib import admin
from django.urls import path, include, re_path

from table.views.auth import registerPage, logout, login_view, infoPageUrls, \
    password_step_first, password_step_second, password_step_lust
from table.views.words import table, delete_word, modify_word
from table.views.get_message import get_message

urlpatterns = [
    # registrations pages
    path('admin/', admin.site.urls),
    path('', registerPage, name='reg'),
    path('logout', logout, name='logout'),
    path('login', login_view, name='login'),
    path('infopage', infoPageUrls, name='info urls'),

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
    re_path(r"\S+/$", registerPage, name="registerPage")

]
