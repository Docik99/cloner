"""
Скрипт выгрузки списка пользователей gitlab

Пример запуска:
python3 gitlab_user_sync.py -g http://localhost:10080 -t yhQvz2QsqXbxakY-zEqC
"""
import random
import json
import argparse

import requests
from prettytable import PrettyTable


def generate_pass(length):
    """Создание пароля"""
    if length <= 0:
        raise Exception("Length of password must be int > 0")

    chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    password = ''
    while len(password) != length:
        password += random.choice(chars)
    return password


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
    parser.add_argument(
        '-f', '--file',
        help='input way to file',
        type=str,
    )
    return parser


def create_file(file_name, file_format, data):
    if file_format == 'json':
        f_json = open(f"{file_name}.{file_format}", "w")
        json.dump(data, f_json)

    elif file_format == 'txt':
        f_txt = open(f"{file_name}.{file_format}", 'w')
        f_txt.write(str(data))

    else:
        raise Exception("The file format must be json or txt")


def create_table(data):
    head = ['email', 'login (name)', 'fullname (username)']
    table = PrettyTable(head)
    for user in data:
        body = [user['email'], user['name'], user['username']]
        table.add_row(body)
    return table


def get_user(arg):
    """Вывод списка пользователей gitlab"""
    response = requests.get(f"{arg.get}/api/v4/users?private_token={arg.token}&per_page=100")

    if response.status_code == 200:
        todos = json.loads(response.text)
        other_web_url = 0
        data_w = []

        for todo in todos:
            data_w.append({'email': todo['email'], 'name': todo['name'], 'username': todo['username']})

            if todo['web_url'].find("gitwork.ru") == -1:
                other_web_url += 1

        return data_w, other_web_url

    else:
        raise Exception(f"Ошибка: {str(response.status_code)}")


def set_user(arg):
    """Создание новых пользователей по данным из json файла"""
    f_json = open(arg.file, 'r')
    todos = json.load(f_json)
    data_w = []

    for todo in todos:
        password = generate_pass(10)
        response = requests.post(f"{arg.set}/api/v4/users?private_token={arg.token}",
                                 {'email': todo['email'], 'name': todo['name'], 'username': todo['username'],
                                  'password': password, 'skip_confirmation': 'true'})
        if response.status_code == 201:
            data_w.append({'username': todo['username'], 'password': password})
            print(f"{todo['username']} : {password}")
        else:
            raise Exception(f"Ошибка: {str(response.status_code)}")

    return data_w


def main():
    """Передача аргументов командной строки исполняемой функции"""
    parsers = create_args()
    args = parsers.parse_args()
    if args.get is not None:
        user_data, other_url = get_user(args)
        table = create_table(user_data)
        create_file('out_of_users', 'json', user_data)
        create_file('out_of_users', 'txt', table)
        print(table)
        print(f"Количество пользователей с web_url, отличающимся от gitwork.ru ---> {str(other_url)}")
    elif args.set is not None:
        create_file('users-pass', 'json', set_user(args))


if __name__ == '__main__':
    main()
