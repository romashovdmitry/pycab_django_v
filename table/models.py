from django.contrib.auth.models import AbstractUser
from django.db import models

# https://stackoverflow.com/questions/54751466/django-does-not-honor-on-delete-cascade


class MyUser(AbstractUser):
    username = models.CharField(unique=True, blank=True, null=True,
                                max_length=200)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class UserInfo(models.Model):
    user_email = models.ForeignKey(MyUser, to_field='email',
                                   on_delete=models.CASCADE,
                                   primary_key=True)
    telegram_id = models.BigIntegerField(null=True, blank=True)
    user_level = models.CharField(max_length=25, null=True, blank=True)


class WholeVocab(models.Model):
    user_email = models.ForeignKey(MyUser, to_field='email',
                                   on_delete=models.CASCADE)
    id_of_word_in_whole = models.BigAutoField(primary_key=True, null=False)
    word_in_whole = models.CharField(max_length=200, null=False)
    definition_of_word_in_whole = models.CharField(max_length=2000, null=True)
    status_of_word_in_whole = models.CharField(max_length=10, blank=True,
                                               null=True)


class DynamicVocab(models.Model):
    user_email = models.ForeignKey(MyUser, to_field='email',
                                   on_delete=models.CASCADE)
    id_of_word_in_dynamic = models.ForeignKey(WholeVocab,
                                            to_field='id_of_word_in_whole',
                                            on_delete=models.CASCADE)
    word_in_dynamic = models.CharField(max_length=200, null=False)
    definition_in_dynamic = models.CharField(max_length=2000, blank=True)
    status_of_word_in_dynamic = models.CharField(max_length=10, null=True)
