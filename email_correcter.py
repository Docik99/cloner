"""
Скрипт изменения email пользователей gitlab

Пример запуска:
python3 email_correcter.py -g http://localhost:10080 -t yhQvz2QsqXbxakY-zEqC
"""

import json
import argparse

import requests


def create_args():
    """Создание аргументов командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u', '--url',
        help='input hostname',
        type=str,
    )
    parser.add_argument(
        '-t', '--token',
        help='input root_token',
        type=str,
    )
    return parser


def get_user(arg):
    """Вывод списка пользователей gitlab"""
    page = 1
    users = []
    while True:
        if arg.url is not None:
            response = requests.get(f"{arg.url}/api/v4/users?private_token={arg.token}&page={page}&per_page=100")
        else:
            response = requests.get(f"https://gitwork.ru/api/v4/users?private_token={arg.token}&page={page}&per_page=100")

        if response.status_code != 200:
            raise Exception(f"Ошибка: {str(response.status_code)}")

        todos = json.loads(response.text)
        print(len(todos))

        for todo in todos:
            users.append({'id': todo['id'], 'username': todo['username']})

        if len(todos) < 100:
            break

        page += 1

    return users


# def corect_email(users):
#     if arg.url is not None:
#         response = requests.get(f"{arg.url}/api/v4/users?private_token={arg.token}&page={page}&per_page=100")
#     else:
#         response = requests.get(f"https://gitwork.ru/api/v4/users?private_token={arg.token}&page={page}&per_page=100")

def main():
    """Передача аргументов командной строки исполняемой функции"""
    parsers = create_args()
    args = parsers.parse_args()
    if args.token is not None:
        get_user(args)
    else:
        print("Не введен токен")


if __name__ == '__main__':
    main()
