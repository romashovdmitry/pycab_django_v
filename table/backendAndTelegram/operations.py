import random
import re
from typing import Tuple

from . import telegram_api_request as tar
from .sql_transactions import SQLTransactions

# Row in tables can have 3 statuses:
# not_done - nothing is happening with row in table
# doing - for deleting of row in table
# modif - for modification of row in table


def show_word(user_email_id):
    '''Foo is using on level "default". Foo show random word from vocab'''
    list_of_records = list(
        SQLTransactions(user_email=user_email_id).selectAllRecordsFromDynamic())
    if len(list_of_records) > 0:
        highest = len(list_of_records)
        pkeys = list(SQLTransactions(
            user_email=user_email_id).selectPkeysFromDynamic())
        random_list = {i: pkeys[i][0] for i in range(highest)}
        random_ = random.randint(1, highest)
        random_ -= 1
        doing = random_list[random_]
        SQLTransactions(status_of_word_in_dynamic='doing',
                        user_email=user_email_id,
                        id_of_word_in_dynamic=doing).setStatudInDynamic()
        del (random_)
        SQLTransactions(
            status_of_word_in_dynamic='doing',
            user_email=user_email_id).selectDynamicDefenitionStatusDoing()
        definition = SQLTransactions(
            user_email=user_email_id).selectDynamicDoing()
        return definition
    return ('Словарь закончился!\n '
            '\nДобавь новые слова или пройдись еще раз по словарю. ')


def vocab_work(user_email_id: int) -> str:
    '''Foo is using on level "default". Foo fills table dynamic_vocab'''
    SQLTransactions(user_email=user_email_id).deleteAllFromDynamicByEmail()
    SQLTransactions(user_email=user_email_id).copyRecordsFromWholeToDynamic()
    return show_word(user_email_id)


def checking_word(message_word: str, email_of_user: str) -> Tuple[bool, str]:
    '''Foo checks accuracy of written (to bot) word'''
    message_word = message_word.rstrip()[::-1].rstrip()[::-1].lower()
    correct_word = SQLTransactions(
        user_email=email_of_user).findWordDynamicStatusDoing()
    SQLTransactions(
        user_email=email_of_user).deleteRecordDynamicStatusDoing()
    if message_word == correct_word.lower():
        return (True, None)
    return (False, correct_word)


def show_all_words_for_deleting(user_email_id, chat_id):
    '''
    Foo is using on level "deleting". Foo returns whole list of words in table 
    whole_vocab. Returning is with a frequency of 25 words. 

    '''
    SQLTransactions(user_email=user_email_id).deleteAllFromDynamicByEmail()
    list_all_words = list(
        SQLTransactions(user_email=user_email_id).selectAllWordsFromWhole())
    if len(list_all_words) < 1:
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
        while len(list_all_words) != 0:
            s = ''
            for b in list_all_words[0:25]:
                s = s + str(i) + '. ' + str(b[0]) + '\n'
                i += 1
            list_all_words = list_all_words[25:]
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


def show_all_words_for_modif(user_email_id: int, chat_id: int):
    '''
    Foo is using on level "modificate word". Foo returns whole list of words in table 
    whole_vocab. Returning is with a frequency of 25 words. 

    '''
    SQLTransactions(user_email=user_email_id).deleteAllFromDynamicByEmail()
    SQLTransactions(user_email=user_email_id).copyRecordsFromWholeToDynamic()
    list_all_words = list(
        SQLTransactions(user_email=user_email_id).selectAllWordsFromDynamic())
    if len(list_all_words) < 1:
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
        while len(list_all_words) != 0:
            s = ''
            for b in list_all_words[0:25]:
                s = s + str(i) + '. ' + str(b[0]) + '\n'
                i += 1
            list_all_words = list_all_words[25:]
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


def delete_word(numbers: str, email_of_user: str) -> str:
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
        list_all_words = list(
            SQLTransactions(
                user_email=email_of_user).selectAllWordsFromWhole())
        numbered_list_of_words = {
            b: list_all_words[b][0] for b in range(len(list_all_words))}
        for b in list_for_deleting:
            SQLTransactions(
                word_in_whole=numbered_list_of_words[b-1],
                user_email=email_of_user).deleteRecordWholeByWord()
        return ('Удалено! ')
    else:
        return ("Пожалуйста, не используйте буквы, предпочтительно "
                "использовать такой формат: \n\n 1, 2, 3")


def modificate_word(message: str, email_of_user: str) -> str:
    '''Foo modificate word and status of word'''
    if (re.search('[a-z]', message)) is None:       # if no letters in message
        message = re.sub('[\s]', '', message)       # remove spaces
        message = int(re.sub('[.,]', '', message))  # remove dots and commas
        try:
            list_all_words = list(SQLTransactions(
                user_email=email_of_user).selectAllWordsFromWhole())
            numbered_list_of_words = {
                b: list_all_words[b][0] for b in range(len(list_all_words))}
            word = numbered_list_of_words[message-1]
            SQLTransactions(
                    word_in_dynamic=word,
                    user_email=email_of_user).setStatusInDynamicModif()
            definition_of_word = SQLTransactions(
                user_email=email_of_user).selectDynamicModif()
            definition_of_word = ("Дефиниция у слова следующая: {}. \nНапиши "
                                  "теперь верную дефиницию.").format(
                                    definition_of_word)
            return definition_of_word
        except Exception as ex:
            return ("Что-то пошло не так. Попробуй, пожалуйста, набрать только"
                    " номер, без других символов. Возможно, в этом дело. "
                    "Exception: {}".format(ex))
    else:
        try:
            number_and_word = message.rsplit('.', 1)
            number_of_word = number_and_word[0]
            word = number_and_word[1].rstrip()[::-1].rstrip()[::-1]
            number_of_word = int(re.sub('[\s]', '', number_of_word))
            pkeys = SQLTransactions(
                user_email=email_of_user).selectPkeysFromDynamic()
            highest = len(pkeys)
            dict_ = {i: pkeys[i][0] for i in range(highest)}
            pkey_of_word = dict_[number_of_word-1]
            SQLTransactions(
                word_in_whole=word,
                rownumber=pkey_of_word
                ).updateWordByPk()
            SQLTransactions(rownumber=pkey_of_word).updateStatusModifInDynamic()
            definition_of_word = SQLTransactions(
                user_email=email_of_user).selectDynamicModif()
            returning_message = ("Слово изменено. Дефиниция у него такая: {}"
                                 "\nНапиши теперь верную дефиницию для слова. "
                                 "Если менять ее не надо, то можешь просто "
                                 "скопировать написанную выше, либо вызвать "
                                 "другую команду. ".format(definition_of_word))
            return (returning_message)
        except Exception:
            return ("Что-то пошло не так. Попробуй еще разок "
                    "именно в формате таком: \n 1. "
                    "Слово. ")


def modificate_definition(definition: str, user_email_id: str) -> str:
    '''Foo modificate definition in row of table whole_vocab '''
    try:
        number_in_whole = SQLTransactions(
            user_email=user_email_id).findRecordPkeyStatusModif()
        SQLTransactions(
            definition=definition,
            id_of_word_in_dynamic=number_in_whole).updateDefinitionInWhole()
        return ('Done!')
    except Exception as ex:
        return ('Что-то пошло не так :(\nEXCEPTION: {}'.format(ex))
