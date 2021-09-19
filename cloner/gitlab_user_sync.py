"""
Скрипт выгрузки списка пользователей gitlab

Примеры запуска:
python3 gitlab_user_sync.py -f out_file g yhQvz2QsqXbxakY-zEqC
gitlab_user_sync.py -f users-data.json s yhQvz2QsqXbxakY-zEqC
"""
import random
import json
import argparse

import requests
from prettytable import PrettyTable


def generate_pass(length):
    """Создание пароля

    Аргументы:
        length: длина пароля

    Возвращаемые значения:
        password: сгенерированный пароль

    """
    if length <= 0:
        raise Exception("Length of password must be int > 0")

    chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    password = ''
    while len(password) != length:
        password += random.choice(chars)
    return password


def create_args():
    """Создание аргументов командной строки

    Возвращаемые значения:
        parser: парсер введенных аргументов

    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'operation',
        help='input "g" for get users or "s" for create users',
        type=str,
    )
    parser.add_argument(
        'token',
        help='input root_token',
        type=str,
    )
    parser.add_argument(
        '-u', '--url',
        help='input hostname (default "https://gitwork.ru")',
        default='https://gitwork.ru',
        type=str,
    )
    parser.add_argument(
        '-f', '--file',
        help='input way to file (required flag if operation = s)',
        type=str,
    )
    return parser


def create_file(file_name, file_format, data):
    """Создает файл с заданым именем, форматом и записывает туда данные

    Аргументы:
        file_name: название файла, который необходимо создать
        file_format: формат файла, который необходисо создать
        data: данные, которые необходимо записать в этот файл

    """
    if file_format == 'json':
        f_json = open(f"{file_name}.{file_format}", "w")
        json.dump(data, f_json)

    elif file_format == 'txt':
        f_txt = open(f"{file_name}.{file_format}", 'w')
        f_txt.write(str(data))

    else:
        raise Exception("The file format must be json or txt")


def create_table(data):
    """Создает таблицу с данными пользователей

    Аргументы:
        data: данные, которые необходимо внести в таблицу

    Возвращаемые значения:
        table: таблица с переданными данными

    """
    head = ['email', 'login (name)', 'fullname (username)']
    table = PrettyTable(head)
    for user in data:
        body = [user['email'], user['name'], user['username']]
        table.add_row(body)
    return table


def get_user(arg):
    """Вывод списка пользователей gitlab

    Аргументы:
        arg: аргументы командной строки

    Возвращаемые значения:
        data_w: данные пользователей, которые необходимо записать в файл
        other_web_url: количество пользователей с доменом отличающимся от gitwork.ru

    """
    response = requests.get(f"{arg.url}/api/v4/users?private_token={arg.token}&per_page=100")

    if response.status_code != 200:
        raise Exception(f"Ошибка: {str(response.status_code)}")

    todos = json.loads(response.text)
    other_web_url = 0
    data_w = []

    for todo in todos:
        data_w.append({'email': todo['email'], 'name': todo['name'],
                       'username': todo['username']})

        if todo['web_url'].find("gitwork.ru") == -1:
            other_web_url += 1

    return data_w, other_web_url


def set_user(arg):
    """Создание новых пользователей по данным из json файла

    Аргументы:
        arg: аргументы командной строки

    Возвращаемые значения:
        data_w: данные новых пользователей (логин - пароль), которые необходимо записать в файл

    """
    f_json = open(arg.file, 'r')
    todos = json.load(f_json)
    data_w = []

    for todo in todos:
        password = generate_pass(10)
        response = requests.post(f"{arg.url}/api/v4/users?private_token={arg.token}",
                                 {'email': todo['email'], 'name': todo['name'],
                                  'username': todo['username'], 'password': password,
                                  'skip_confirmation': 'true'})
        if response.status_code == 201:
            data_w.append({'username': todo['username'], 'password': password})
            print(f"{todo['username']} : {password}")
        else:
            raise Exception(f"Ошибка: {str(response.status_code)}")

    return data_w


def main():
    """Передача аргументов командной строки исполняемым функциям"""
    parsers = create_args()
    args = parsers.parse_args()
    if args.operation == 'g':
        user_data, other_url = get_user(args)
        table = create_table(user_data)
        if args.file is None:
            create_file('out_of_users', 'json', user_data)
            create_file('out_of_users', 'txt', table)
        else:
            create_file(args.file, 'json', user_data)
            create_file(args.file, 'txt', table)
        print(table)
        print(f"Количество пользователей с web_url,"
              f" отличающимся от gitwork.ru ---> {str(other_url)}")
    elif args.operation == 's':
        if args.file is not None:
            create_file('users-pass', 'json', set_user(args))
        else:
            print("Укажите файл со списком пользователей, которых необходимо создать!")


if __name__ == '__main__':
    main()
