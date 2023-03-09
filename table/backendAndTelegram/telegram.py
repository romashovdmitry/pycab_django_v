from . import operations
from . import telegram_api_request as tar
from .buttonPatterns import patterns
from .hash import hashing
from table.models import MyUser, UserInfo, WholeVocab, DynamicVocab

def requests_list(message: str, telegram_id: int):
    '''
    Foo takes message and telegram_id from Telegram server
    and make an answer to user.
    There are 4 main levels, every level means a certain
    step in work of Telegram Bot.

    This foo is more like a distributor of functions, that realy have a weight,
    do action. Also first lines of foo check authorization of user in Bot.

    '''
    if message == '/start':
        return tar.ButtonCreate(message_text='Привет! Напиши свою почту. ',
                                chat_id=telegram_id,
                                texts_of_button=['']).return_button()
    try:
        if not UserInfo.objects.filter(telegram_id=telegram_id).exists():
            if '@' in message:
                    user = MyUser.objects.filter(email=message).first()
                    user_info = UserInfo.objects.get(user_email=message)
                    user_info.user_level = 'start password'
                    user_info.telegram_id = telegram_id
                    user_info.save()
                    return tar.ButtonCreate(message_text='Кажется, ты написал почту. '
                                            'Теперь напиши пароль',
                                            chat_id=telegram_id,
                                            texts_of_button=['']).return_button()
            else:
                return tar.ButtonCreate(message_text='Напиши почту, '
                                        'которую ты зарегистрировал '
                                        'на сайте. Именно почту.\n '
                                        'Если не зарегистрирован, то '
                                        'следуте зарегистрироваться '
                                        'сначала. Ссылка на сайт: '
                                        'https://telegrampyvocab.herokuapp.com/registration',
                                        chat_id=telegram_id,
                                        texts_of_button=['']).return_button()
        
        user = UserInfo.objects.filter(telegram_id=telegram_id).first().user_email

        if UserInfo.objects.filter(telegram_id=telegram_id).first().user_level is not None:
            user_info = UserInfo.objects.filter(telegram_id=telegram_id).first()
            email_of_user = user_info.user_email
            level = user_info.user_level
            message_list = ['Добавить новое слово',
                            'Удалить слова',
                            'Внести изменения в словарь',
                            'Проверять слова!'
                            ]
            if message in message_list:
                if message == "Добавить новое слово":
                    patterns(message=message, chat_id=telegram_id,
                             user_email=email_of_user).add_word()
                elif message == 'Удалить слова':
                    patterns(message, telegram_id, email_of_user).delete_word()
                elif message == 'Внести изменения в словарь':
                    patterns(message, telegram_id, email_of_user).modif_dict()
                elif message == 'Проверять слова!':
                    patterns(message, telegram_id, email_of_user).check_word()
            elif level == 'start password':
                try:
                    if hashing(message) == user.password:
                        user_info.user_level = 'default'
                        user_info.save()
                        return tar.ButtonCreate(message_text='Ты авторизован! '
                                                'Теперь добавь первое '
                                                'слово. '
                                                'Нажми кнопку. ',
                                                chat_id=telegram_id,
                                                texts_of_button=['Добавить '
                                                                 'новое слово']).\
                            return_button()
                    else:
                        tar.ButtonCreate(message_text="Пароль не тот :("
                                                      "\nПопробуй еще раз, "
                                                      "пожалуйста. ",
                                         chat_id=telegram_id,
                                         texts_of_button=['']).\
                            return_button()
                except Exception:
                    tar.ButtonCreate(message_text='Что-то пошло не так. '
                                                  'Посмотри внимательно свой '
                                                  'пароль. Напиши снова почту',
                                                  chat_id=telegram_id,
                                                  texts_of_button=['']).\
                        return_button()
            elif level == 'adding word':
                WholeVocab.objects.filter(user_email=email_of_user).update(status_of_word_in_whole='not done')
                whole_vocab_string = WholeVocab()
                whole_vocab_string.add_new_string(
                    word=message.rstrip()[::-1].rstrip()[::-1],
                    user=user
                )
                whole_vocab_string.new_level('doing')
                user_info.user_level = 'adding_definition'
                user_info.save()
                tar.ButtonCreate(message_text='Напиши дефиницию или '
                                              'перевод данного слова.',
                                 chat_id=telegram_id,
                                 texts_of_button=['Добавить новое слово',
                                                  'Удалить слова',
                                                  'Внести изменения '
                                                  'в словарь']).\
                    return_button()
            elif level == 'adding_definition':
                whole_vocab_string = WholeVocab.objects.filter(
                    user_email=email_of_user).filter(
                    status_of_word_in_whole='doing').first()
                whole_vocab_string.definition_of_word_in_whole = message.rstrip()[::-1].rstrip()[::-1]
                whole_vocab_string.save()
                user_info.user_level = 'default'
                user_info.save()
                tar.ButtonCreate(message_text='Новое слово добавлено.',
                                 chat_id=telegram_id,
                                 texts_of_button=['Добавить новое слово',
                                                  'Проверять слова!',
                                                  'Внести изменения в словарь',
                                                  'Удалить слова'], ).\
                    return_button()
            elif level == 'default':
                bul, word = operations.checking_word(message, email_of_user)
                if bul is True:
                    mes = 'Правильно. ' + '\n\n' + \
                        operations.show_word(email_of_user)
                    tar.ButtonCreate(message_text=mes,
                                     chat_id=telegram_id,
                                     texts_of_button=['Добавить новое слово',
                                                      'Внести изменения в '
                                                      'словарь',
                                                      'Удалить слова',
                                                      'Проверять слова!']).\
                        return_button()
                else:
                    text = f'Неправильно.\nПравильно так: {word} \n\n'
                    mes = f'{text} {operations.show_word(email_of_user)}'
                    tar.ButtonCreate(message_text=mes,
                                     chat_id=telegram_id,
                                     texts_of_button=['Добавить новое слово',
                                                      'Внести изменения '
                                                      'в словарь',
                                                      'Удалить слова',
                                                      'Проверять слова!']).\
                        return_button()
            elif level == 'deleting':
                wholevocab = WholeVocab.objects.filter(user_email=email_of_user).all()
                if len(wholevocab) > 0:
                    delete_message = operations.delete_word(
                        numbers=message,
                        user_email=email_of_user)
                    if "Пожалуйста" in delete_message:
                        tar.ButtonCreate(message_text='Пожалуйста, не '
                                                      'используйте буквы, '
                                                      'предпочтительно '
                                                      'использовать '
                                                      'такой формат: '
                                                      '\n\n 1, 2, 3',
                                         chat_id=telegram_id,
                                         texts_of_button=['Добавить новое '
                                                          'слово',
                                                          'Проверять слова!',
                                                          'Внести изменения в '
                                                          'словарь']).\
                            return_button()
                    else:
                        tar.ButtonCreate(message_text='Удалено!',
                                         chat_id=telegram_id,
                                         texts_of_button=['Добавить новое '
                                                          'слово',
                                                          'Проверять слова!',
                                                          'Внести изменения в '
                                                          'словарь',
                                                          'Удалить слова']).\
                            return_button()
                else:
                    tar.ButtonCreate(message_text='Словарь в данный момент '
                                                  'пустой.\n\nНеловко это '
                                                  'сообщать, но сначала '
                                                  'следует добавить слова '
                                                  'прежде, чем удалять их :) ',
                                                  chat_id=telegram_id,
                                                  texts_of_button=['Добавить новое слово',
                                                                   'Проверять слова!',
                                                                   'Внести изменения в словарь',
                                                                   'Удалить слова']).return_button()
            elif level == 'modificate word':
                definition = operations.modificate_word(message, email_of_user)
                if 'Что-то пошло не так' in definition:
                    tar.ButtonCreate(message_text=definition,
                                     chat_id=telegram_id,
                                     texts_of_button=['']).return_button()
                else:
                    user_info.user_level = 'modificate definition'
                    user_info.save()
                    tar.ButtonCreate(message_text=definition,
                                     chat_id=telegram_id,
                                     texts_of_button=['Добавить новое слово',
                                                      'Удалить слова',
                                                      'Проверять слова!',
                                                      'Внести изменения '
                                                      'в словарь']).\
                        return_button()
            elif level == 'modificate definition':
                result_of_operation = operations.modificate_definition(
                    message, email_of_user)
                tar.ButtonCreate(message_text=result_of_operation,
                                 chat_id=telegram_id,
                                 texts_of_button=['Добавить новое слово',
                                                  'Удалить слова',
                                                  'Проверять слова!',
                                                  'Внести изменения в словарь']
                                 ).return_button()
    except Exception as ex:
        tar.ButtonCreate(message_text=ex,
                         chat_id=telegram_id,
                         texts_of_button=['']).\
            return_button()
