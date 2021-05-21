"""
Скрипт изменения email пользователей gitlab

Пример запуска:
python3 email_correcter.py -u http://localhost:10080 -t yhQvz2QsqXbxakY-zEqC
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
    """Формирование списка пользователей с неправильной почтой"""
    users_on_page = 100
    page = 1
    users = []
    while True:
        response = requests.get(f"{arg.url}/api/v4/users?private_token={arg.token}"
                                f"&page={page}&per_page={users_on_page}")

        if response.status_code != 200:
            raise Exception(f"Ошибка: {str(response.status_code)}")

        todos = json.loads(response.text)
        for todo in todos:
            if todo['email'] != todo['username'] + '@gitwork.ru':
                users.append({'id': todo['id'], 'username': todo['username']})

        if len(todos) < 100:
            break

        page += 1

    return users


def correct_email(arg, users):
    """Изменение почты у заданных пользователей"""
    error_users = []

    for user in users:
        email = user['username'] + '@gitwork.ru'

        if arg.url is None:
            arg.url = 'https://gitwork.ru'

        response = requests.put(f"{arg.url}/api/v4/users/{user['id']}?private_token={arg.token}",
                                {'email': email})

        if response.status_code != 200:
            error_users.append({'id': user['id'], 'username': user['username']})

    return error_users


def main():
    """Передача аргументов командной строки исполняемой функции"""
    parsers = create_args()
    args = parsers.parse_args()
    if args.token is not None:
        if args.url is None:
            args.url = 'https://gitwork.ru'
        users = get_user(args)
        error_users = correct_email(args, users)
        print(f"Email адрес успешно изменен у {len(users) - len(error_users)}"
              f" пользователей из {len(users)}")
        if len(error_users) != 0:
            print("Список пользователей у которых не удалось изменить email: ")
            for error in error_users:
                print(error['username'])
    else:
        print("Не введен токен")


if __name__ == '__main__':
    main()
