"""
Скрипт изменения email пользователей gitlab

Пример запуска:
python3 email_correcter.py -u http://localhost:10080 -t yhQvz2QsqXbxakY-zEqC
"""

import json
import argparse

import requests


def create_args():
    """Создание аргументов командной строки

    Возвращаемые значения:
        parser: парсер введенных аргументов

    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u', '--url',
        help='input hostname (default "https://gitwork.ru")',
        default='https://gitwork.ru',
        type=str,
    )
    parser.add_argument(
        'token',
        help='input root_token',
        type=str,
    )
    return parser


def get_user(arg, domen):
    """Формирование списка пользователей с неправильной почтой

    Аргументы:
        arg: аргументы командной строки
        domen: домен почты, который должен быть у всех пользователей

    Возвращаемые значения:
        users: список пользователей с неправильным доменом почты

    """
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
            if todo['email'] != todo['username'] + domen:
                users.append({'id': todo['id'], 'username': todo['username']})

        if len(todos) < 100:
            break

        page += 1

    return users


def correct_email(arg, users, domen):
    """Изменение почты у заданных пользователей

    Аргументы:
        arg: аргументы командной строки
        users: список пользователей с неправильным доменом почты
        domen: домен почты, который должен быть у всех пользователей

    Возвращаемые значения:
        error_users: список пользователей, у которых не удалось изменить почту

    """
    error_users = []

    for user in users:
        email = user['username'] + domen

        response = requests.put(f"{arg.url}/api/v4/users/{user['id']}?private_token={arg.token}",
                                {'email': email})

        if response.status_code != 200:
            error_users.append({'id': user['id'], 'username': user['username']})

    return error_users


def main():
    """Передача аргументов командной строки исполняемой функции"""
    parsers = create_args()
    args = parsers.parse_args()
    domen = "@gitwork.ru"
    users = get_user(args, domen)
    error_users = correct_email(args, users, domen)
    print(f"Email адрес успешно изменен у {len(users) - len(error_users)}"
          f" пользователей из {len(users)}")
    if len(error_users) != 0:
        print("Список пользователей у которых не удалось изменить email: ")
        for error in error_users:
            print(error['username'])


if __name__ == '__main__':
    main()
