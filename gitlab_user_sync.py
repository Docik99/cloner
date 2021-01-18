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


def get_user(args):
    """Вывод списка пользователей gitlab"""
    response = requests.get('http://' + args.get + '/api/v4/users?private_token=' + args.token)

    if response.status_code == 200:
        for user in response.json():
            print()
            for param in user:
                print(str(param) + ': ' + str(user[param]))
        return 0
    else:
        print('Ошибка: ' + str(response.status_code))
        return 1


if __name__ == '__main__':
    parsers = create_args()
    args = parsers.parse_args()
    get_user(args)
