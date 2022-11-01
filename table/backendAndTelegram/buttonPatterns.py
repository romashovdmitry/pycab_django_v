from . import operations, telegram_api_request
from .sql_transactions import SQLTransactions

my_email_error = [None]
my_password_error = [None]


class patterns:
    '''
    Class forms:
    1. Buttons.
    2. Text of answer from Bot.
    3. Level.
    Yes, we form that not only by using this class, but there are in class most
    frequently used cases. That's like standart combinations.
    '''

    def __init__(self, message, chat_id, user_email_id):
        # инициализируем атрибуты
        self.message = message
        self.chat_id = chat_id
        self.user_email_id = user_email_id

    def make_req(self, dict_of_communication):
        # формируем атрибуты для запроса и меняем уровень
        texts_of_button = dict_of_communication.get(self.message)['buttons']
        level = dict_of_communication.get(self.message)['level']
        SQLTransactions(user_level=level,
                        user_email=self.user_email_id).updateUserLevel()
        message_text = dict_of_communication.get(self.message)['message_text']
        telegram_api_request.ButtonCreate(
            message_text=message_text,
            chat_id=self.chat_id,
            texts_of_button=texts_of_button).return_button()

    def add_word(self):
        # в каждом случае делаем специиальный словарь, из которого берутся
        # кнопки для формирования кнопок
        dict_of_add = {
            'Добавить новое слово': {
                'buttons': [
                    'Проверять слова!',
                    'Добавить новое слово',
                    'Удалить слова',
                    'Внести изменения в словарь'
                ],
                'message_text': 'Напиши слово',
                'level': 'adding word'
            }
        }
        self.make_req(dict_of_add)

    def delete_word(self):
        dict_of_delete = {
            'Удалить слова': {
                'buttons': [
                    'Проверять слова!',
                    'Добавить новое слово',
                    'Внести изменения в словарь'
                ],
                'message_text': operations.show_all_words_for_deleting(
                    self.user_email_id,
                    self.chat_id
                    ),
                'level': 'deleting'
            }
        }
        self.make_req(dict_of_delete)

    def modif_dict(self):
        dict_of_modif = {
            'Внести изменения в словарь': {
                'buttons': [
                    'Добавить новое слово',
                    'Удалить слова',
                    'Проверять слова!'
                ],
                'message_text': operations.show_all_words_for_modif(
                    self.user_email_id,
                    self.chat_id
                    ),
                'level': 'modificate word'
            }
        }
        self.make_req(dict_of_modif)

    def check_word(self):
        dict_of_check = {
            'Проверять слова!': {
                'buttons': [
                    'Добавить новое слово',
                    'Внести изменения в словарь',
                    'Удалить слова'
                ],
                'message_text': operations.vocab_work(self.user_email_id),
                'level': 'default',
            }
        }
        self.make_req(dict_of_check)
