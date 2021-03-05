"""
Скрипт выгрузки списка пользователей gitlab

Пример запуска:
python3 gitlab_user_sync.py -g http://localhost:10080 -t yhQvz2QsqXbxakY-zEqC
"""
import argparse
import requests
import json
import gitlab
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
    parser.add_argument(
        '-s', '--set',
        help='input hostname',
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

def set_user(arg):
    response = requests.post(arg.set + '/api/v4/users?private_token=' + arg.token, {'email':'lox2@gitwork.ru', 'name':'lox2', 'username':'lox2', 'password':'12345678'}) # через стандартные запросы
    print(response.status_code)

    # с использованием библиотеки gitlab
    # gl = gitlab.Gitlab(arg.set, private_token=arg.token)
    # user = gl.users.create({'email': 'pervonah@gitwork.ru', 'password': '12345678',
    #                         'username': 'lox',
    #                         'name': 'pervonah'})

def main():
    """Передача аргументов командной строки исполняемой функции"""
    parsers = create_args()
    args = parsers.parse_args()
    if args.get is not None: get_user(args)
    if args.set is not None: set_user(args)


if __name__ == '__main__':
    main()
