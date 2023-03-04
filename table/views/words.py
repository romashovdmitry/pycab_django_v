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
from ..models import MyUser, UserInfo, WholeVocab, DynamicVocab

# custom classes
from ..backendAndTelegram.hash import hashing
from ..backendAndTelegram.sql_transactions import SQLTransactions


# redis
from ..tasks import py_send_mail

# etc libs
import json
import os
from dotenv import load_dotenv


# Create your views here.

@login_required(login_url='login')
def table(request):
    # request.user is email of user
    email_adress = str(request.user)
    if request.method == 'POST':
        # form = Form(request.POST) так надо сделать
        word = request.POST.get('word')
        definition = request.POST.get('definition')
        whole_vocab_string = WholeVocab()
        whole_vocab_string.add_new_string(
            word=word,
            definition=definition,
            user=request.user
        )
        messages.info(request, f'Word {word} is added!')
        word, definition = None, None  # вот это надо заменить form_cleaned()
        return redirect('table')
    records = WholeVocab.objects.filter(user_email=email_adress).all()
    return render(request, 'table.html', {'records': records})


def modify_word(request, pk):
    try:
        if request.method == 'POST':
            word = request.POST.get('word')
            definition = request.POST.get('definition')
            session_pk = int(request.session['pk'].replace(' ', ''))
            del request.session['pk']
            vocab_string = WholeVocab.objects.filter(
                id_of_word_in_whole=session_pk).first()
            vocab_string.update_string(
                word=word,
                definition=definition
            )
            messages.info(request, f'Word {word} is changed!')
            return redirect('table')
        request.session['pk'] = pk
        vocab_string = WholeVocab.objects.get(id_of_word_in_whole=pk)
        print(f'\n\nHELLO {vocab_string}\n\n')
        word_and_definition = {
            'word': vocab_string.word_in_whole,
            'definition': vocab_string.definition_of_word_in_whole
        }
        return render(request, 'modify_word.html', {
            'word_and_definition': word_and_definition
        })
    except Exception:
        return HttpResponse("SOMETHING SHIT HAPPENS!")


def delete_word(request, pk):
    table_string = WholeVocab.objects.get(id_of_word_in_whole=int(pk))
    word = table_string.word_in_whole
    table_string.delete()
    messages.info(request, f'Word {word} is deleted!')
    return redirect('table')