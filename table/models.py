# Django imports
from django.db.models import ForeignKey, UUIDField, CharField, DateTimeField
from django.db.models import Model, CASCADE

# Python imports
import uuid

# import custom classes
from users.models import MyUser


class Vocab(Model):

    class Meta:
        db_table = 'vocab'
        unique_together = [['word', 'definition']]

    user_email = ForeignKey(MyUser,
                            to_field='email',
                            on_delete=CASCADE)
    id = UUIDField(
        default=uuid.uuid4, primary_key=True, null=False)
    created_at = DateTimeField(auto_now_add=True)
    word = CharField(max_length=256,
                     null=False,
                     verbose_name='Word')
    definition = CharField(max_length=2048,
                           null=True,
                           verbose_name='Definition')
    status_of_word_in_whole = CharField(max_length=10,
                                        blank=True,
                                        null=True)

    def new_level(self, status):

        self.status_of_word_in_whole = status
        self.save()

    def add_new_string(self, user, word=None, definition='no definition :('):

        self.word = word
        self.definition = definition
        self.user_email = user
        self.save()

    def update_string(self, word, definition):

        self.word = word
        self.definition = definition
        self.save()


class DynamicVocab(Model):

    class Meta:
        db_table = 'dynamic_vocab'

    user_email = ForeignKey(MyUser, to_field='email',
                            on_delete=CASCADE)
    id_dynamic = ForeignKey(Vocab,
                            to_field='id',
                            on_delete=CASCADE)
    word_dynamic = CharField(max_length=256, null=False)
    definition_dynamic = CharField(max_length=2048, blank=True)
    status_of_word_dynamic = CharField(max_length=10, null=True)

    def new_record(self, email, record):

        self.user_email = email
        self.word_dynamic = record.word_in_whole
        self.definition_dynamic = record.definition_of_word_in_whole
        self.id_of_word_in_dynamic = record
        self.save()
