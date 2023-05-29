from django.core.management import BaseCommand

import requests

import os
from dotenv import load_dotenv
load_dotenv()


class Command(BaseCommand):
    '''Foo creates list if best posts '''

    def handle(self, *args, **options):

        set_webhook = f'https://api.telegram.org/bot{os.getenv("TELEGRAM_TOKEN")}/setWebhook?url={os.getenv("HOST")}/telegram'
        delete_webhook = f'https://api.telegram.org/bot{os.getenv("TELEGRAM_TOKEN")}/deleteWebhook'

        requests.post(url=delete_webhook)
        requests.post(url=set_webhook)