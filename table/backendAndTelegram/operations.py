import random
import re
from typing import Tuple

from . import telegram_api_request as tar

from table.models import Vocab, DynamicVocab
from users.models import MyUser, UserInfo

# Row in tables can have 3 statuses:
# not_done - nothing is happening with row in table
# doing - for deleting of row in table
# modif - for modification of row in table


def show_word(user_email):
    '''Foo is using on level "default". Foo show random word from vocab'''
    list_of_records = DynamicVocab.objects.filter(user_email=user_email).all()
    if len(list_of_records) > 0:
        highest = len(list_of_records)
        pkeys = [b.id_dynamic.id for b in list_of_records]
        random_list = {i: pkeys[i] for i in range(highest)}
        # PLACE
        # FOR
        # ENUMERATE
        random_ = random.randint(1, highest)
        random_ -= 1
        doing = random_list[random_]
        _ = Vocab.objects.get(id=doing)
        dynamic_table_string = DynamicVocab.objects.get(
            id_dynamic=_)
        dynamic_table_string.status_of_word_dynamic = 'doing'
        dynamic_table_string.save()
        del (random_)
        return dynamic_table_string.definition_dynamic
    return ('Словарь закончился!\n '
            '\nДобавь новые слова или пройдись еще раз по словарю. ')


def vocab_work(user_email) -> str:
    '''Foo is using on level "default". Foo fills table dynamic_vocab'''
    DynamicVocab.objects.all().delete()
    whole_vocab_records = Vocab.objects.filter(
        user_email=user_email).all()
    for record in whole_vocab_records:
        _ = DynamicVocab()
        _.new_record(
            email=user_email,
            record=record
        )
    return show_word(user_email)


def checking_word(message_word: str, user_email: str) -> Tuple[bool, str]:
    '''Foo checks accuracy of written (to bot) word'''
    message_word = message_word.rstrip()[::-1].rstrip()[::-1].lower()
    dynamic_table_string = DynamicVocab.objects.get(
        user_email=user_email, status_of_word_dynamic='doing')
    correct_word = dynamic_table_string.word_dynamic
    dynamic_table_string.delete()
    if message_word == correct_word.lower():
        return (True, None)
    return (False, correct_word)


def show_all_words_for_deleting(user_email, chat_id):
    '''
    Foo is using on level "deleting". Foo returns whole list of words in table 
    whole_vocab. Returning is with a frequency of 25 words. 

    '''
    DynamicVocab.objects.all().delete()
    all_words = Vocab.objects.filter(user_email=user_email).all()
    if len(all_words) < 1:
        tar.ButtonCreate(message_text="Словарь пустой.\n"
                                      "Сначала следует "
                                      "добавить слова.",
                                      chat_id=chat_id,
                                      texts_of_button=["Добавить новое ",
                                                       "слово",
                                                       "Проверять слова!",
                                                       "Внести "
                                                       "изменения в "
                                                       "словарь"]). \
            return_button()
    else:
        i = 1
        while len(all_words) != 0:
            s = ''
            for b in all_words[0:25]:
                s = s + str(i) + '. ' + str(b.word) + '\n'
                i += 1
            all_words = all_words[25:]
            tar.ButtonCreate(message_text=s,
                             chat_id=chat_id,
                             texts_of_button=['']).return_button()
        tar.ButtonCreate(message_text='Это список слов.\n\n'
                                      'Напиши номер слова, которое хочешь '
                                      'удалить.\n\nЕсли их '
                                      'несколько, то напиши '
                                      'через запятую '
                                      'в таком формате: '
                                      '1,2,3',
                                      chat_id=chat_id,
                                      texts_of_button=['Добавить новое '
                                                       'слово',
                                                       'Проверять слова!',
                                                       'Внести изменения в'
                                                       ' словарь']). \
            return_button()


def show_all_words_for_modif(user_email: int, chat_id: int):
    '''
    Foo is using on level "modificate word". Foo returns whole list of words in table 
    whole_vocab. Returning is with a frequency of 25 words. 

    '''
    DynamicVocab.objects.all().delete()
#    SQLTransactions(user_email=user_email).deleteAllFromDynamicByEmail()

    whole_vocab_records = Vocab.objects.filter(
        user_email=user_email).all()
    for record in whole_vocab_records:
        _ = DynamicVocab()
        _.new_record(
            email=user_email,
            record=record
        )
    all_dynamica_words = DynamicVocab.objects.filter(
        user_email=user_email).all()
    if len(all_dynamica_words) < 1:
        tar.ButtonCreate(message_text='Словарь пустой.\n '
                                      'Сначала следует '
                                      'добавить слова.',
                                      chat_id=chat_id,
                                      texts_of_button=['Добавить новое '
                                                       'слово',
                                                       'Проверять слова!',
                                                       'Внести изменения '
                                                       'в словарь',
                                                       'Удалить слова']). \
            return_button()
    else:
        i = 1
        while len(all_dynamica_words) != 0:
            s = ''
            for b in all_dynamica_words[0:25]:
                s = s + str(i) + '. ' + str(b.word_dynamic) + '\n'
                i += 1
            all_dynamica_words = all_dynamica_words[25:]
            tar.ButtonCreate(message_text=s,
                             chat_id=chat_id,
                             texts_of_button=['']).return_button()
        tar.ButtonCreate(message_text='Это список слов.\nНапиши номер слова, '
                                      'которое изменить. Если хочешь изменить '
                                      'само слово, не только его дефиницию, то'
                                      ' то напиши сразу слово. Например так:'
                                      '\n1. Example word',
                                      chat_id=chat_id,
                                      texts_of_button=['Добавить новое '
                                                       'слово',
                                                       'Проверять слова!',
                                                       'Внести изменения '
                                                       'в словарь',
                                                       'Удалить слова']). \
            return_button()


def delete_word(numbers: str, user_email: str) -> str:
    '''Foo delete row from table'''
    alpha_checking = (re.search('[^1-9, ]', numbers))
    if alpha_checking is None:                        # if there is no letters
        numbers = re.sub('[\s]', '', numbers)         # delete spaces
        # create list, comma is separator
        list_for_deleting = numbers.rsplit(',')
        list_for_deleting = list((int(i) for i in list_for_deleting))
        list_for_deleting.sort()
        if list_for_deleting[0] > list_for_deleting[-1]:
            list_for_deleting.reverse()
        all_words = Vocab.objects.filter(user_email=user_email).all()
        numbered_list_of_words = {
            b: all_words[b].id for b in range(len(all_words))}
        for b in list_for_deleting:
            table_string = Vocab.objects.get(
                id=numbered_list_of_words[b-1],
                user_email=user_email
            )
            table_string.delete()
        return ('Удалено! ')
    else:
        return ("Пожалуйста, не используйте буквы, предпочтительно "
                "использовать такой формат: \n\n 1, 2, 3")


def modificate_word(message: str, user_email: str) -> str:
    '''Foo modificate word and status of word'''
    if (re.search('[a-z]', message)) is None \
            and (re.search('[а-я]', message)) is None:       # if no letters in message
        message = re.sub('[\s]', '', message)       # remove spaces
        message = int(re.sub('[.,]', '', message))  # remove dots and commas
        try:
            all_whole_vocab_words = Vocab.objects.filter(
                user_email=user_email).all()
            numbered_list_of_words = {
                b: all_whole_vocab_words[b].word for b in range(len(all_whole_vocab_words))}
            word = numbered_list_of_words[message-1]
            dynamic_table_string = DynamicVocab.objects.get(
                user_email=user_email, word_dynamic=word)
            dynamic_table_string.status_of_word_dynamic = 'modif'
            dynamic_table_string.save()
            definition_of_word = dynamic_table_string.definition_dynamic
            definition_of_word = ("Дефиниция у слова следующая:\n\n"
                                  f"{definition_of_word}. \n\nНапиши "
                                  "теперь верную дефиницию.")
            return definition_of_word
        except Exception as ex:
            return ("Что-то пошло не так. Попробуй, пожалуйста, набрать только"
                    " номер, без других символов. Возможно, в этом дело. "
                    f"Exception: {ex}")
    else:
        try:
            number_and_word = message.rsplit('.', 1)
            number_of_word = number_and_word[0]
            word = number_and_word[1].rstrip()[::-1].rstrip()[::-1]
            number_of_word = int(re.sub('[\s]', '', number_of_word))
            list_of_records = DynamicVocab.objects.filter(
                user_email=user_email).all()
            pkeys = [
                b.id_dynamic.id for b in list_of_records]
            highest = len(pkeys)
            dict_ = {i: pkeys[i] for i in range(highest)}
            pkey_of_word = dict_[number_of_word-1]

            whole_vocab_string = Vocab.objects.get(
                id=pkey_of_word)
            whole_vocab_string.word = word
            whole_vocab_string.save()

            dynamic_table_string = DynamicVocab.objects.get(
                id_dynamic=pkey_of_word)
            dynamic_table_string.status_of_word_dynamic = 'modif'
            dynamic_table_string.save()

            definition_of_word = dynamic_table_string.definition_dynamic

            returning_message = ("Слово изменено. Дефиниция у него такая: \n\n"
                                 f"{definition_of_word}\n\n"
                                 "Напиши теперь верную дефиницию для слова. "
                                 "Если менять ее не надо, то можешь просто "
                                 "скопировать написанную выше, либо вызвать "
                                 "другую команду. ")
            return (returning_message)
        except Exception:
            return ("Что-то пошло не так. Попробуй еще разок "
                    "именно в формате таком: \n 1. "
                    "Слово. ")


def modificate_definition(definition: str, user_email: str) -> str:
    '''Foo modificate definition in row of table whole_vocab '''
    try:
        dynamic_table_string = DynamicVocab.objects.get(
            user_email=user_email,
            status_of_word_dynamic='modif'
        )
        number_in_whole = dynamic_table_string.id_dynamic.id
        whole_table_string = Vocab.objects.get(
            id=number_in_whole,
            user_email=user_email
        )
        whole_table_string.definition = definition
        whole_table_string.save()
        return ('Done!')
    except Exception as ex:
        return (f'Что-то пошло не так :(\nEXCEPTION: {ex}')
