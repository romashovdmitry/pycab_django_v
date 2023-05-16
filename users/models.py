# Django imports
from django.contrib.auth.models import AbstractUser
from django.db.models import UUIDField, EmailField, DateTimeField, ForeignKey, BigIntegerField, CharField
from django.db.models import Model, Index, CASCADE

# Python imports
import uuid


class MyUser(AbstractUser):

    first_name = last_name = is_superuser = is_staff = username = None

    class Meta:

        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            Index(fields=['email'], name='user_email_index')
        ]

    id = UUIDField(default=uuid.uuid4, primary_key=True)
    email = EmailField(unique=True)
    created_at = DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    # i'm not going to use Django Admin
#    REQUIRED_FIELDS = ['username']


class UserInfo(Model):

    class Meta:
        db_table = 'user_info'

    user_email = ForeignKey(MyUser, to_field='email',
                            on_delete=CASCADE)
    telegram_id = BigIntegerField(null=True, blank=True)
    user_level = CharField(max_length=25, null=True, blank=True)
