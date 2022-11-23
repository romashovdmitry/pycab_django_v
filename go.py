import requests

ngrok = '2bb3-217-76-11-135.eu.ngrok.io'

useremail = 'new@gmail.com'
userpassword = 'new'
url = f'https://{ngrok}/api/auth'
auth_answer = requests.post(url=url, json={"email": 'new@gmail.com', 'password' : userpassword})
print(auth_answer.json())

'''
url = f'https://{ngrok}/api/create'

data = {'word_in_whole': 'test api', 'definition_of_word_in_whole':'hop hey lala ley', 'user_email':'new@gmail.com'}

kek = requests.post(url=url, json=data)
print(kek.json())
'''