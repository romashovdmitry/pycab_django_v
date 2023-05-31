# Value of project

The project aims to enhance English vocabulary by saving new words with definitions and facilitating training through random dispatching in a Telegram Bot. The core of the project revolves around Django routes, PostgreSQL, and the Telegram Bot.

To gain a better understanding of the project, you can watch a screencast of the working project by following the link below:

[ScreenCast of working project](https://www.youtube.com/watch?v=Kjbo7WEAOno)

## Technology Stack: 

The project utilizes the following technologies:

- SQL commands, PostgreSQL, Django ORM
- Telegram API
- JSON, requests (python HTTP library)
- Regular expressions
- Django, Django-packages, Jinja syntax
- Formatting strings
- Redis as a message-broker for Celery
- Network knowledge, such as WebHooks and SSH for testing  
- HTML, Bootstrap, CSS
- Hashing
- Object-Oriented Programming (OOP)
- Docker
- Deploy on remote machine, Nginx to proxy requests, webhooks
- CI/CD with GitHub Actions

# How To Run on local machine

Run the Ngrok server to create a secure tunnel to your local development environment. Execute the following command:

<code>ngrok http 8000</code> 

If you encounter any errors related to user rights, use the command

<code>.\ngrok http 8000</code>

Take domen of the Ngrok URL, which will be something like <code>https://2fd1-83-139-27-28.eu.ngrok.io </code>

Create .env (look at .env_example), open the .env file and set the Ngrok URL as the value for the NGROK variable in the settings.py file. Replace the existing value with the Ngrok URL you obtained in the previous step. Additionally, make sure to set other environment variables in the .env file according to your requirements. For example:

<code>EMAIL_HOST_USER = 'yoursmail@gmail.com'
EMAIL_HOST_PASSWORD = 'yourspassword'</code>

Note: The email host user and password variables may vary depending on the email service you are using.

Run the following command to start the Docker container:

<code>docker compose up</code>

Find the ID of the Django-docker container by executing the command: 

<code>docker ps</code>

Enter the container by running the following command

<code>docker exec -t -i id_of_container bash</code>

Set up the webhook by running the make_webhook_firstly.py script

<code>python3 make_webhook_firstly.py</code>

Finally, open <code>http://127.0.0.1:8000/</code> in your browser to access and interact with the application.

# Project Structure

The project consists of two main parts:

1. Telegram bot.

The Telegram bot functionality is implemented in the telegram.py file. It includes the requests_list function, which processes incoming messages in the Telegram bot. By using a "flag" (level) code, the requests_list function selects functions from the operations.py module and utilizes them to construct responses for the user. For the design of the web interface, we have utilized simple HTML and Bootstrap styles. You can learn more about Bootstrap styles https://getbootstrap.comю 

2. Django Web Interface.

The Django web interface provides a user-friendly interface to interact with the application. The URLs and views for the web interface are organized in their respective folders. For the design of the web interface, we have utilized simple HTML and Bootstrap styles. You can learn more about Bootstrap styles

## Next steps in project: 

1. Implement Simple Math Models for Improved Word Selection. Currently, the output of words in the project is entirely random. To enhance the user experience, consider adding simple math models that prioritize certain words over others. By introducing mathematical algorithms or techniques, you can make the word selection process more intelligent and ensure that difficult words are not neglected. This will help users remember a broader range of vocabulary.

2. Enhance the project's functionality by incorporating word parsing capabilities from the Oxford Dictionary website or integrating with a suitable API.

last and the most importatnt: Resolve bugs, of course (:
