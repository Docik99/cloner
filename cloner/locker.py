
import json
import argparse

import requests


def create_args():
    """Создание аргументов командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--set',
        help='input hostname',
        type=str,
    )
    parser.add_argument(
        '-t', '--token',
        help='input root_token',
        type=str,
    )
    parser.add_argument(
        '-f', '--file',
        help='input way to file',
        type=str,
    )
    return parser


def lock_user(arg):
    """Блокировка пользователей по данным из json файла"""
    global user_id
    f_json = open(arg.file, 'r') #файл, содержащий name пользователей
    todos = json.load(f_json)
    count_users = 0
    block_users = 0

    for todo in todos:
        count_users += 1
        response_get = requests.get(arg.set + '/api/v4/users?username=' + todo['name'])
        if response_get.status_code == 200:
            datas = json.loads(response_get.text)
            for data in datas:
                user_id = data['id']
            print(user_id)
        else:
            print("Error GET: " + str(response_get.status_code))

        response_post = requests.post(arg.set + '/api/v4/users/' + str(user_id) + '/block?private_token=' + arg.token)
        if response_post.status_code == 201:
            block_users += 1
        else:
            print("Error POST: " + str(response_post.status_code))

    if count_users == block_users:
        print("All users are block")


def main():
    """Передача аргументов командной строки исполняемой функции"""
    parsers = create_args()
    args = parsers.parse_args()
    if args.set is not None:
        lock_user(args)


if __name__ == '__main__':
    main()
