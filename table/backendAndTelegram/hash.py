import hashlib

import os
from dotenv import load_dotenv
load_dotenv()


def hashing(password):
    ''' Foo hashs password entered by user '''
    password_start = os.getenv('PASSWORD_START')
    password_finish = os.getenv('PASSWORD_FINISH')
    password = password_start + password + password_finish
    password = password.encode('utf-8')
    password = hashlib.sha256((password)).hexdigest()
    salt = password[3:6]
    salt = salt.encode('utf-8')
    password = password.encode('utf-8')
    hashed_password = hashlib.pbkdf2_hmac(
        hash_name='sha256', password=password, salt=salt, iterations=100000)
    return (hashed_password.hex())

