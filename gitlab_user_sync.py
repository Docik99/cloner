"""
Скрипт выгрузки списка пользователей gitlab

Пример запуска:
python3 gitlab_user_sync.py -g http://localhost:10080 -t yhQvz2QsqXbxakY-zEqC
"""
import argparse
import requests
import json
from prettytable import PrettyTable
import random


def generate_pass():
    """Создание пароля"""
    chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    length = 10  # длина пароля
    password = ''
    for n in range(length):
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


def get_user(arg):
    """Вывод списка пользователей gitlab"""
    response = requests.get(arg.get + "/api/v4/users?private_token=" + arg.token + "&per_page=100")

    if response.status_code == 200:
        todos = json.loads(response.text)
        head = ['login (name)', 'fullname (username)']
        table = PrettyTable(head)
        other_web_url = 0
        f_json = open("out_of_users.json", "w")
        f_json.write('[')
        counter = 0

        for todo in todos:
            counter += 1
            data = {'email': todo['email'], 'name': todo['name'], 'username': todo['username']}
            json.dump(data, f_json)
            if counter != len(todos): #чтобы в конце не было запятой
                f_json.write(',')

            body = [todo['name'], todo['username']]
            table.add_row(body)

            if todo['web_url'].find("gitwork.ru") == -1:
                other_web_url += 1

        f_json.write(']')
        f_txt = open('out_of_users.txt', 'w')
        f_txt.write(str(table))
        print(table)
        print("Количество пользователей с web_url, отличающимся от gitwork.ru ---> " + str(other_web_url))

    else:
        print("Ошибка: " + str(response.status_code))


def set_user(arg):
    f_json = open(arg.file, 'r')
    todos = json.load(f_json)
    pass_json = open('users-pass.json', 'w')
    pass_json.write('[')
    counter = 0

    for todo in todos:
        password = generate_pass()
        response = requests.post(arg.set + '/api/v4/users?private_token=' + arg.token,
                                 {'email': todo['email'], 'name': todo['name'], 'username': todo['username'],
                                  'password': password, 'skip_confirmation': 'true'})
        if response.status_code == 201:
            counter += 1
            data = {'username': todo['username'], 'password': password}
            json.dump(data, pass_json)
            if counter != len(todos):  # чтобы в конце не было запятой
                pass_json.write(',')

            print(todo['username'] + ' : ' + password)

        else:
            print("Ошибка: " + str(response.status_code))

    pass_json.write(']')


def main():
    """Передача аргументов командной строки исполняемой функции"""
    parsers = create_args()
    args = parsers.parse_args()
    if args.get is not None:
        get_user(args)
    elif args.set is not None:
        set_user(args)


if __name__ == '__main__':
    main()
