# built-in django packages
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, redirect, render

# custom django classes
from table.forms import myForm
from table.models import MyUser, UserInfo

# custom classes
from table.backendAndTelegram.hash import hashing

# redis
from table.tasks import py_send_mail

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
            login(request, user)

            new_user_info = UserInfo()
            new_user_info.user_email = user
            new_user_info.save()

            messages.info(request, f'Account for {user.email} is added!')
            return redirect('info urls')
        else:
            messages.error(request, "anything go wrong :( Please, try again. ")
            form = myForm()
            return render(request, 'auth_pages/user_register.html', {'form': form})
    if request.user.is_authenticated:
        return redirect('table')
    form = myForm()
    return render(request, 'auth_pages/user_register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        if MyUser.objects.filter(email=email).exists():
            password = request.POST.get('password')
            user = MyUser.objects.get(email=email)
            true_password = user.password
            if hashing(password) == true_password: 
                login(request, user)
                return redirect('table')
            else:
                messages.error(request, "Wrong password :(")
        else:
            messages.error(request, "Didn't find this email :(")
    form = myForm()
    return render(request, 'auth_pages/user_login.html', {'form': form})


def password_step_first(request):
    if request.method == 'POST':
        em = request.POST.get('email')
        if MyUser.objects.filter(email=em).exists():
            request.session['email-for-user'] = em
            password = MyUser.objects.filter(email=em).first().password
            fake_password = str(password[:10])[::-1]
            request.session['fake_password'] = fake_password
            py_send_mail.delay(
                adress=em, code=fake_password)
            return render(request, 'password_step_second.html')
        else:
            return HttpResponse(f'ther is no this email: {em}')
    return render(request, 'password_step_first.html')


def password_step_second(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        fake_password = request.session['fake_password']
        em = request.session['email-for-user']
        if password == fake_password:
            #            del request.session['fake_password']
            return render(request, 'password_step_lust.html')
    return HttpResponse('nope')


def password_step_lust(request):
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
