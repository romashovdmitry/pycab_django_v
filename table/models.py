from django.contrib.auth.models import AbstractUser
from django.db import models

# https://stackoverflow.com/questions/54751466/django-does-not-honor-on-delete-cascade


class MyUser(AbstractUser):

    class Meta:
        db_table = 'users'

    username = models.CharField(unique=True, blank=True, null=True,
                                max_length=200)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class UserInfo(models.Model):

    class Meta:
        db_table = 'user_info'

    user_email = models.ForeignKey(MyUser, to_field='email',
                                   on_delete=models.CASCADE,
                                   primary_key=True)
    telegram_id = models.BigIntegerField(null=True, blank=True)
    user_level = models.CharField(max_length=25, null=True, blank=True)


class WholeVocab(models.Model):

    class Meta:
        db_table = 'whole_vocab'

    user_email = models.ForeignKey(MyUser,
                                   to_field='email',
                                   on_delete=models.CASCADE)
    id_of_word_in_whole = models.BigAutoField(primary_key=True,
                                              null=False)
    word_in_whole = models.CharField(max_length=200,
                                     null=False)
    definition_of_word_in_whole = models.CharField(max_length=2000,
                                                   null=True)
    status_of_word_in_whole = models.CharField(max_length=10,
                                               blank=True,
                                               null=True)

    def new_level(self, status):
        self.status_of_word_in_whole = status
        self.save()

    def add_new_string(self, user, word=None, definition=None):
        self.word_in_whole = word
        self.definition_of_word_in_whole = definition
        self.user_email = user
        self.save()

    def update_string(self, word, definition):
        self.word_in_whole = word
        self.definition_of_word_in_whole = definition
        self.save()


class DynamicVocab(models.Model):

    class Meta:
        db_table = 'dynamic_vocab'

    user_email = models.ForeignKey(MyUser, to_field='email',
                                   on_delete=models.CASCADE)
    id_of_word_in_dynamic = models.ForeignKey(WholeVocab,
                                              to_field='id_of_word_in_whole',
                                              on_delete=models.CASCADE)
    word_in_dynamic = models.CharField(max_length=200, null=False)
    definition_in_dynamic = models.CharField(max_length=2000, blank=True)
    status_of_word_in_dynamic = models.CharField(max_length=10, null=True)

    def new_record(self, email, record):
        self.user_email = email
        self.word_in_dynamic = record.word_in_whole
        self.definition_in_dynamic = record.definition_of_word_in_whole
        self.id_of_word_in_dynamic = record
        self.save()

