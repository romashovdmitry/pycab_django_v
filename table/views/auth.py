# delete imports after modifications
from sqlalchemy import create_engine

# built-in django packages 
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, redirect, render
from django.views.decorators.csrf import csrf_exempt

# custom django classes
from ..forms import myForm
from ..models import MyUser, UserInfo

# custom classes
from ..backendAndTelegram.hash import hashing
from ..backendAndTelegram.sql_transactions import SQLTransactions
from ..backendAndTelegram.telegram import requests_list

# redis
from ..tasks import py_send_mail

# etc libs
import json
import os
from dotenv import load_dotenv


# Create your views here.


@login_required(login_url='login')
def infoPageUrls(request):
    return render(request, 'infopage_urls.html')


def registerPage(request):
    if request.method == 'POST':
        form = myForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.password = hashing(user.password)
            user.save()
            form.save()
            login(request, user)

            new_user_info = UserInfo()
            new_user_info.user_email = user
            new_user_info.save()

            messages.info(request, f'Account for {user.email} is added!')
            return redirect('info urls')
        else:
            messages.error(request, "anything go wrong :( Please, try again. ")
            form = myForm()
            return render(request, 'user_register.html', {'form': form})
    if request.user.is_authenticated:
        return redirect('table')
    form = myForm()
    return render(request, 'user_register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = myForm(request.POST)
        form_email = form['email']
        if MyUser.objects.filter(email=form_email).exists():
            email = request.POST.get('email').lower()
            password = form['password']
            user = MyUser.objects.get(email=email)
            true_password = user.password
            if hashing(password) == true_password: 
                login(request, user)
            else:
                messages.error(request, "Didn't find this data :(")
        else:
            messages.error(request, "Didn't find this data :(")
            return render(request, 'infopage_urls.html') if hashing(password) == true_password else HttpResponse('nope login')
    form = myForm()
    return render(request, 'user_login.html', {'form': form})

def passwordstepone(request):
    if request.method == 'POST':
        em = request.POST.get('email')
        if MyUser.objects.filter(email=em).exists():
            request.session['email-for-user'] = em
            password = MyUser.objects.filter(email=em).first().password
            fake_password = str(password[:10])[::-1]
            request.session['fake_password'] = fake_password
            py_send_mail.delay(
                adress=em, code=fake_password)
            return render(request, 'passwordsteptwo.html')
        else:
            return HttpResponse(f'ther is no this email: {em}')
    return render(request, 'passwordstepone.html')


def passwordsteptwo(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        fake_password = request.session['fake_password']
        em = request.session['email-for-user']
        if password == fake_password:    
#            del request.session['fake_password']
            return render(request, 'passwordsteplust.html')
    return HttpResponse('nope')


def passwordsteplust(request):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        new_password = hashing(new_password)
        em = request.session['email-for-user']
#        del request.session['email-for-user']
        user = MyUser.objects.get(email=em)
        user.password = new_password
        user.save()
        login(request, user)
        messages.info(request, f'Password for {user.email} is modified!')
        return redirect('login')

def logout(request):
    user_logout(request)
    return redirect('login')