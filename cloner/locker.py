"""
Скрипт блокировки пользователей по списку

Пример запуска: python3 locker.py -u https://host.ru yhQvz2QsqXbxakY-zEqC file.json
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
    parser.add_argument(
        'file',
        help='input way to file',
        type=str,
    )
    return parser


def lock_user(arg):
    """Блокировка пользователей по данным из json файла

    Аргументы:
        arg: аргументы командной строки

    """
    user_id = 0
    f_json = open(arg.file, 'r') #файл, содержащий name пользователей
    todos = json.load(f_json)
    count_users = 0
    block_users = 0

    for todo in todos:
        count_users += 1
        response_get = requests.get(f"{arg.set}/api/v4/users?username={todo['name']}")
        if response_get.status_code == 200:
            datas = json.loads(response_get.text)
            for data in datas:
                user_id = data['id']
            print(user_id)
        else:
            print(f"Error GET: {str(response_get.status_code)}")

        response_post = requests.post(f"{arg.set}/api/v4/users/{str(user_id)}"
                                      f"/block?private_token={arg.token}")
        if response_post.status_code == 201:
            block_users += 1
        else:
            print(f"Error POST: {str(response_post.status_code)}")

    if count_users == block_users:
        print("All users are block")


def main():
    """Передача аргументов командной строки исполняемой функции"""
    parsers = create_args()
    args = parsers.parse_args()
    lock_user(args)


if __name__ == '__main__':
    main()
