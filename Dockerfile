FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY webhook.py ./
RUN pip uninstall django
RUN pip install -r requirements.txt
COPY crontab ./
RUN chmod 600 crontab