"""
Скрипт выгрузки списка пользователей gitlab

Пример запуска:
python3 gitlab_user_sync.py -g http://localhost:10080 -t yhQvz2QsqXbxakY-zEqC
"""
import argparse
import requests
import json
from prettytable import PrettyTable


def create_args():
    """Создание аргументов командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-g', '--get',
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
    response = requests.get(arg.get + "/api/v4/users?private_token=" + arg.token)

    if response.status_code == 200:
        todos = json.loads(response.text)
        head = ['id', 'fullname (username)', 'login (name)']
        table = PrettyTable(head)
        other_web_url = 0
        for todo in todos:
            body = [todo['id'], todo['username'], todo['name']]
            table.add_row(body)
            if todo['web_url'].find("gitwork.ru") == -1:
                other_web_url += 1

        print(table)
        print("Количество пользователей с web_url, отличающимся от gitwork.ru ---> " + str(other_web_url))

    else:
        print("Ошибка: " + str(response.status_code))


def main():
    """Передача аргументов командной строки исполняемой функции"""
    parsers = create_args()
    args = parsers.parse_args()
    get_user(args)


if __name__ == '__main__':
    main()
