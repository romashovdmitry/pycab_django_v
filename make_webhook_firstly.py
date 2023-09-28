import requests

import os
from dotenv import load_dotenv
load_dotenv()

print({os.getenv("HOST")})

set_webhook = f'https://api.telegram.org/bot{os.getenv("TELEGRAM_TOKEN")}/setWebhook?url={os.getenv("HOST")}/telegram'
delete_webhook = f'https://api.telegram.org/bot{os.getenv("TELEGRAM_TOKEN")}/deleteWebhook'


print("\nGOGOOG\n")
print(delete_webhook)
print(set_webhook)
y = requests.post(url=delete_webhook)
print(y.status_code)
x = requests.post(url=set_webhook)
print(x.status_code)
print("\nwebhook done\n")
