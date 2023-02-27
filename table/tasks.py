from email.message import EmailMessage
from celery import shared_task
from django.core.mail import send_mail
import smtplib
import ssl

import os
from dotenv import load_dotenv
load_dotenv()

@shared_task
def py_send_mail(code, adress):

    sender = os.getenv('EMAIL_HOST_USER')
    reciever = 'romashov.dmitry.o@gmail.com'
    gmail_password = os.getenv('EMAIL_HOST_PASSWORD')

    em = EmailMessage()
    em['From'] = 'romashov.dmitry.py@gmail.com'
    em['To'] = 'romashov.dmitry.o@gmail.com'
    em['subject'] = 'hello'
    em.set_content("Your's Code For Pycab")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, gmail_password)
        smtp.sendmail(sender, reciever, em.as_string)
