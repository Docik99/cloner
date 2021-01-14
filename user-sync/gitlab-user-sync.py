import requests
import argparse

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

def main():
    """Вывод списка пользователей gitlab"""
    parser = create_args()
    args = parser.parse_args()
    response = requests.get('http://' + args.get + '/api/v4/users?private_token=' + args.token)
    print(response.status_code)

    if response.status_code == 200:
        print('Усепх')
        print(response.json())
    else:
        print('Ошибка')


if __name__ == '__main__':
    main()
