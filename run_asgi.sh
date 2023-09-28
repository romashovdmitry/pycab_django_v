#!/bin/bash
python manage.py runserver 0.0.0.0:8000
#daphne -b 127.0.0.1 -p 8001 pycab.asgi:application