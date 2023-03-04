"""pycab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from table.views.auth import registerPage, logout, login_view, infoPageUrls, \
    passwordstepone, passwordsteptwo, passwordsteplust
from table.views.words import table, delete_word, modify_word
from table.views.get_message import get_message

#    path('5630063573:AAGMtKDZiz8Eigwkw8JZXJR2F2yEIM-U6rQ', views.get_message, name='telegram request'),

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
    path('newpasswordstepone', passwordstepone, name='passwordstepone'),
    path('passwordsteptwo', passwordsteptwo, name='passwordsteptwo'),
    path('passwordsteplust', passwordsteplust, name='passwordsteplust'),

    # api url
    path('api/', include('table.api.urls')),

    # for Telegram webhook url
    path('telegram', get_message)

]
