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

    sender = EMAIL_HOST_USER
    reciever = 'romashov.dmitry.o@gmail.com'
    gmail_password = EMAIL_HOST_PASSWORD

    em = EmailMessage()
    em['From'] = sender
    em['To'] = reciever
    em['subject'] = "hello, your's code!"
    em.set_content(f"Your's Code For Pycab: {code}")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, gmail_password)
        smtp.sendmail(sender, reciever, em.as_string)
