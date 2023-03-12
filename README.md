# Value of project

Project is created for improving English vocabulary by saving new words with definitions and training by random dispatching in Telegram Bot. Core of project consist of Django routes, PostgreSQL and Telegram Bot. 

It's better for more understanding to watch video in link bellow:

[ScreenCast of working project](https://www.youtube.com/watch?v=Kjbo7WEAOno)

## Stack of technologies: 
- SQL commands, PostgreSQL, Django ORM
- Telegram API
- JSON, requests (python HTTP library)
- regular expressions
- Django, Django-packages, Jinja syntax
- formatting strings
- Redis as message-broker for Celery
- network knowledge, like WebHook, SSH for testing  
- HTML, Bootstrap, CSS
- Hashing
- OOP
- Docker


# How To Run on local machine

Run Ngrok server by

<code>ngrok http 8000</code> or if you get error abount rights of user<code>.\ngrok http 8000</code>

Get domain of ngrok's URL. Example: 

<code>https://2fd1-83-139-27-28.eu.ngrok.io </code>

Open .env file and set domain in variable NGROK in settings.py. Remember that you need to have telegram bot for using app and also set values in other .env variables before next steps. Set your's adress and password instead of EMAIL configuration variables. 

<code>EMAIL_HOST_USER = 'yoursmail@gmail.com'
EMAIL_HOST_PASSWORD = 'yourspassword'</code>

These two variables could be depend on used service.

Run docker-compose command 

<code>docker compose up</code>

Find Django-docker container id by command 

<code>docker ps</code>

Come in container

<code>docker exec -t -i id_of_container bash</code>

And set webhook firstly by command

<code>python3 make_webhook_firstly.py</code>

Open in your's browser <code>http://127.0.0.1:8000/</code> and enjoy. 

# Python code

Mainly, project consists of 2 parts:

1. Telegram bot.
2. Django Interface. 

URLs and views are in their respective folders, telegram.py include function requests_list, that processes incoming messages in Telegram bot. Mainly by using "flag" (level) code choose functions from module operations.py and use them to construct answers for user. 

# Django Web Interface

For web interface have used simple HTML and Bootstrap styles: https://getbootstrap.com

## Next steps in project: 

1. To add simple math models for less random output of words. Now output is absolutely random. That's not cool, because to remember some words are more easily than others. And if you have 1000 words, than difficult words just can not to be showed in Telegram bot. 
2. Division any certain amount of words on pages (pagination). Like on one page could be maximum 100 words. Because if you have 1000 words, loading of page could be very slow. 
