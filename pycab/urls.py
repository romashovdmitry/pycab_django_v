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
from django.urls import path

from table import views

urlpatterns = [
    path('5630063573:AAGMtKDZiz8Eigwkw8JZXJR2F2yEIM-U6rQ', views.get_message, name='telegram request'),
    path('admin/', admin.site.urls),
    path('registration/', views.registerPage, name='reg'),
    path('logout', views.logout, name='logout'),
    path('login', views.login_view, name='login'),
    path('infopage', views.infoPageUrls, name='info urls'),
    path('table', views.table, name='table'),
    path('delete_word/<pk>', views.delete_word, name='delete'),
    path('modify/<pk>', views.modify_word, name='modify'),
    path('check', views.check, name='check'),
    path('newpasswordstepone', views.passwordstepone, name='passwordstepone'),
    path('passwordsteptwo', views.passwordsteptwo, name='passwordsteptwo'),
    path('passwordsteplust', views.passwordsteplust, name='passwordsteplust')
]


