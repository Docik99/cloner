"""
Скрипт выгрузки списка пользователей gitlab
"""
import argparse
import requests


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
    response = requests.get('http://' + arg.get + '/api/v4/users?private_token=' + arg.token)

    if response.status_code == 200:
        for user in response.json():
            print()
            for param in user:
                print(str(param) + ': ' + str(user[param]))
    else:
        print('Ошибка: ' + str(response.status_code))


def main():
    """Передача аргументов командной строки исполняемой функции"""
    parsers = create_args()
    args = parsers.parse_args()
    get_user(args)


if __name__ == '__main__':
    main()
