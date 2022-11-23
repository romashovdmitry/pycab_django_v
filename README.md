# How To Run

Run docker-compose command 

<code>docker compose up</code>

Run Ngrok server by

<code>ngrok http 8000</code> or if you get error abount rights of user<code>.\nhrok http 8000</code>

Get domain of ngrok's URL. Example: 

<code>79a6-2a02-2a57-a268-0-4d6d-3846-5680-87df.eu.ngrok.io </code>

Set domain in variable NGROK in settings.py. There is link in line 14 for making WebHook. Set domain instead of <code>NGROK</code>. 
Remember that you need to have telegram bot for using app. 

Set your's adress and password instead of EMAIL configuration variables in the end of settings.py. 

<code>
EMAIL_HOST_USER = 'yoursmail@gmail.com'
EMAIL_HOST_PASSWORD = 'yourspassword'
</code>

Open in your's browser <code>https://ngrokdomain/registration</code> and enjoy. 

# Python code

Mainly, project consists of 2 parts:

1. Telegram bot.
2. Django Interface. 

URLs and views are in their respective folders, telegram.py include function requests_list, that processes incoming messages in Telegram bot. Mainly by using "flag" (level) code choose functions from module operations.py and use them to construct answers for user. 

# Flask Web Interface

For web interface have used simple HTML and Bootstrap styles: https://getbootstrap.com

## Next steps in project: 

1. To add simple math models for less random output of words. Now output is absolutely random. That's not cool, because to remember some words are more easily than others. And if you have 1000 words, than difficult words just can not to be showed in Telegram bot. 
2. Division any certain amount of words on pages (pagination). Like on one page could be maximum 100 words. Because if you have 1000 words, loading of page could be very slow. 
3. To add password recovery by email. 

## Stack of technologies: 
- SQL commands, PostgreSQL
- Telegram API
- JSON, requests
- little bit of regular expressions
- Django, Django-packages, Jinja syntax
- formatting strings
- Redis as message-broker for Celery
- little bit of network knowledge, like WebHook, SSH for testing  
- HTML, Bootstrap, CSS
- Hashing
- OOP
- Docker
