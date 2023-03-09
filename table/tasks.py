from email.message import EmailMessage
from celery import shared_task
from django.core.mail import send_mail
import smtplib
import ssl
from pycab.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

import os
from dotenv import load_dotenv
load_dotenv()


@shared_task
def py_send_mail(code, adress):

    send_mail(
        subject="New password for Romashov Pycab",
        message=f'Code: {code}',
        from_email=EMAIL_HOST_USER,   # This will have no effect is you have set DEFAULT_FROM_EMAIL in settings.py
        recipient_list=[adress],    # This is a list
        fail_silently=False     # Set this to False so that you will be noticed in any exception raised
    )