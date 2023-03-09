# delete imports after modifications
from sqlalchemy import create_engine

# built-in django packages
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, redirect, render

# custom django classes
from table.forms import vocabRecord
from table.models import WholeVocab

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
    form = vocabRecord()
    records = WholeVocab.objects.filter(user_email=email_adress).all()
    return render(request, 'table_pages/table.html', {'records': records, 'form': form})


# https://stackoverflow.com/questions/526457/django-form-fails-validation-on-a-unique-field
def modify_word(request, pk):
    try:
        if request.method == 'POST':
            vocab_string = WholeVocab.objects.get(id_of_word_in_whole=pk)
            form = vocabRecord(request.POST, instance=vocab_string)
            if form.is_valid():
                form.save()
                messages.info(request, f'Word {vocab_string.word_in_whole}'
                              ' is changed!')
                return redirect('table')
        vocab_string = WholeVocab.objects.get(id_of_word_in_whole=pk)
        form = vocabRecord(instance=vocab_string)
        return render(request, 'table_pages/modify_word.html', {
            'form': form,
            'pk': pk
        })
    except Exception:
        return HttpResponse("SOMETHING SHIT HAPPENS!")


def delete_word(request, pk):
    table_string = WholeVocab.objects.get(id_of_word_in_whole=int(pk))
    word = table_string.word_in_whole
    table_string.delete()
    messages.info(request, f'Word {word} is deleted!')
    return redirect('table')
