import requests

import os
from dotenv import load_dotenv
load_dotenv()

set_webhook = f'https://api.telegram.org/bot{os.getenv("TELEGRAM_TOKEN")}/setWebhook?url={os.getenv("HOST")}/telegram'
delete_webhook = f'https://api.telegram.org/bot{os.getenv("TELEGRAM_TOKEN")}/deleteWebhook'

requests.post(url=delete_webhook)
x = requests.post(url=set_webhook)
print('webhook done')