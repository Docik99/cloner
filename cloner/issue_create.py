"""
Скрипт создания issue с паролем для пользователя в репозитории timp

python3 issue_create.py -u https://gitwork.ru -t AzJqh2AKxVC_Wj9pn_T8 -f users-pass.json
"""

import json
import argparse

import requests


def create_args():
    """Создание аргументов командной строки"""
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


def create_issue(arg):
    """Создание issue в репе timp"""
    f_json = open(arg.file, 'r')
    todos = json.load(f_json)
    for todo in todos:
        have_timp = False
        response = requests.get(f"{arg.url}/api/v4/users/{str(todo['username'])}"
                                f"/projects/?private_token={arg.token}&simple=true")
        if response.status_code == 200:
            projects = json.loads(response.text)
            for project in projects:
                if project['name'] == 'timp':
                    have_timp = True
                    new_issue = requests.post(f"{arg.url}/api/v4/projects/{str(project['id'])}/issues/?private_token={arg.token}", {'title': 'you new password', 'description': todo['password']})
                    if new_issue.status_code == 201:
                        print('Успех, новое ишью создано!')
                    else:
                        print(f'Ошибка: {str(new_issue.status_code)}')
            if not have_timp:
                print(f"У пользователя {todo['username']} отсутствует репозиторий timp!")
        else:
            print(response.status_code)


def main():
    """Передача аргументов командной строки исполняемой функции"""
    parsers = create_args()
    args = parsers.parse_args()
    create_issue(args)


if __name__ == '__main__':
    main()
