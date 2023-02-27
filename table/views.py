import json
from sqlalchemy import create_engine

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .backendAndTelegram.hash import hashing
from .backendAndTelegram.sql_transactions import SQLTransactions
from .backendAndTelegram.telegram import requests_list
from .forms import myForm
from .models import MyUser
from .tasks import py_send_mail

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
            db = create_engine(
                'postgresql://postgres:polkabulok56@pgdb:5432/pycab_django_db')
            conn = db.connect()
            db.execute("INSERT INTO table_userinfo "
                       "(user_email_id) "
                       "VALUES ('{}');".format(user.email))
            conn.close()
            messages.info(request, f'Account for {user.email} is added!')
            return redirect('info urls')
        else:
            messages.error(request, "anything go wrong :( Please, try again. ")
            form = myForm()
            return render(request, 'register_form.html', {'form': form})
    if request.user.is_authenticated:
        return redirect('table')
    form = myForm()
    return render(request, 'register_form.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = myForm(request.POST)
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        user = MyUser.objects.get(email=email)
        true_password = user.password
        print(f'True password: {true_password}')
        if hashing(password) == true_password: 
            login(request, user)
        return render(request, 'infopage_urls.html') if hashing(password) == true_password else HttpResponse('nope login')
    form = myForm()
    return render(request, 'login_page.html', {'form': form})

@csrf_exempt
def get_message(request):
    '''URL to get data(from request) from Telegram server'''
    try:
        if request.method == 'POST':
            formatted_request = HttpResponse(request).content.decode('utf-8')
            formatted_request = json.loads(formatted_request)
            message = formatted_request['message']['text']
            chat_id = formatted_request['message']['chat']['id']
            requests_list(message, chat_id)
            return HttpResponse(status=200)
    except Exception as ex:
        return HttpResponse("Bot Don't Work, Look At views.get_message. \
                            Exception: {}".format(ex))


@login_required(login_url='login')
def table(request):
    # есть объект request.user - это почта юзера
    email_adress = str(request.user)
    print(dir(request))
    if request.method == 'POST':
        word = request.POST.get('word')
        definition = request.POST.get('definition')
        SQLTransactions(
            word_in_whole=word, definition=definition,
            user_email=email_adress).addWordDefinitionInWhole()
        messages.info(request, f'Word {word} is added!')
        word, definition = None, None
        return redirect('table')
    records = SQLTransactions(
        user_email=email_adress).selectAllInWholeVocabByEmail()
    records = records
    return render(request, 'table.html', {'records': records})


def modify_word(request, pk):
    try:
        if request.method == 'POST':
            email_adress = str(request.user)
            word = request.POST.get('word')
            definition = request.POST.get('definition')
            session_pk = request.session['pk']
            del request.session['pk']
            SQLTransactions(
                word_in_whole=word, definition=definition,
                rownumber=session_pk).updateWordDefinitionInWhole()
            messages.info(request, f'Word {word} is changed!')
            records = SQLTransactions(
                user_email=email_adress).selectAllInWholeVocabByEmail()
            records = records
            return render(request, 'table.html', {'records': records})
        request.session['pk'] = pk
        word = SQLTransactions(rownumber=pk).getWordFromWhole()
        definition = SQLTransactions(rownumber=pk).getDefinitionWholeByPK()
        wd = {'word': word, 'definition': definition}
        return render(request, 'modify_word.html', {'wd': wd})
    except Exception:
        return HttpResponse("HERE MUST BE ERROR PAGE")


def delete_word(request, pk):
    word = SQLTransactions(rownumber=pk).getWordFromWhole()
    SQLTransactions(rownumber=pk).deleteRecordWholeByPkey()
    messages.info(request, f'Word {word} is deleted!')
    return redirect('table')


def passwordstepone(request):
    if request.method == 'POST':
        em = request.POST.get('email')
        if SQLTransactions(user_email=em).validateEmailInTable():
            request.session['email-for-user'] = em
            password = SQLTransactions(user_email=em).getPasswordOfUser()
            fake_password = str(password[:10])[::-1]
            request.session['fake_password'] = fake_password
            em = request.session['email-for-user']
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
        SQLTransactions(password=new_password, user_email=em).setNewPassword()
        user = MyUser.objects.get(email=em)
        login(request, user)
        messages.info(request, f'Password for {user.email} is modified!')
        return redirect('login')

def logout(request):
    user_logout(request)
    return redirect('login')


def check(request):
    if request.user.is_authenticated:
        return HttpResponse('yes')
    else:
        return HttpResponse('nope')