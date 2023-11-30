#! /usr/bin/env python3

import requests
import os
import random
import string
import json
import threading
import logging
from requests.exceptions import SSLError, ConnectionError


def load_json_file(file_path):
    with open(file_path) as file:
        return json.load(file)


def generate_random_name(names):
    event = random.randint(0, 4)
    if event == 0:
        return random.choice(names).lower()
    elif event in [1, 2]:
        separator = ['-', '.', '_']
        return random.choice(names).lower() + random.choice(separator) + random.choice(names).lower()
    else:
        return random.choice(names).lower() + random.choice(string.digits) + random.choice(string.digits)


def generate_random_password(chars, dictionary, names):
    event = random.randint(0, 6)
    if event == 0:
        return ''.join(random.choices(chars, k=random.randint(7, 15)))
    elif event in [1, 2]:
        return ''.join(random.choices(dictionary, k=2)) + random.choice(string.digits)
    elif event in [3, 4]:
        return random.choice(dictionary) + random.choice(string.digits)
    else:
        return random.choice(string.digits) + random.choice(dictionary) + random.choice(names)


def run(url, formDataNameLogin, formDataNamePass, email_domains, chars, dictionary, names):
    session = requests.Session()
    while True:
        username = generate_random_name(
            names) + '@' + random.choice(email_domains)
        password = generate_random_password(chars, dictionary, names)
        try:
            response = session.post(url, allow_redirects=False, data={
                formDataNameLogin: username,
                formDataNamePass: password,
            })
            logging.info(
                f'[Result: {response.status_code}] -- [USERNAME: {username}] -- [PASSWORD: {password}]')
        except (SSLError, ConnectionError) as e:
            logging.error(f'Connection error: {e}')
        except Exception as e:
            logging.error(f'Error: {e}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    url = input('Form URL: ')
    formDataNameLogin = input('Form Data [Account/Email] Name: ')
    formDataNamePass = input('Form Data Password Name: ')
    threads_count = int(input('Threads: '))

    chars = string.ascii_letters + string.digits
    random.seed(os.urandom(1024))

    names = load_json_file('assets/names.json')
    email_domains = load_json_file('assets/email_domains.json')
    dictionary = load_json_file('assets/dictionary.json')

    threads = []
    for i in range(threads_count):
        t = threading.Thread(target=run, args=(
            url, formDataNameLogin, formDataNamePass, email_domains, chars, dictionary, names))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()
