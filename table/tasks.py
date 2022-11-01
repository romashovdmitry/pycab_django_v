from email.message import EmailMessage
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def py_send_mail(code, adress):

    send_mail(
        subject="New password for Romashov Pycab",
        message=f'Code: {code}',
        from_email="romashov.dmitry.o@gmail.com",   # This will have no effect is you have set DEFAULT_FROM_EMAIL in settings.py
        recipient_list=[adress],    # This is a list
        fail_silently=False     # Set this to False so that you will be noticed in any exception raised
    )
