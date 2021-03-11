import gitlab
import argparse
import requests
import json

def create_args():
    """Создание аргументов командной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--serv',
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


def create_issue(arg):
    f_json = open(arg.file, 'r')
    todos = json.load(f_json)
    for todo in todos:
        response = requests.get(arg.serv + "/api/v4/users/" + str(todo['username']) + "/projects/?private_token=" + arg.token + "&simple=true")
        if response.status_code == 200:
            todoss = json.loads(response.text)
            for tod in todoss:
                print(tod)
        else:
            print(response.status_code)
            # нужно найти id проекта тимп у нужного пользователя а затем по этому id создать ишью

def main():
    """Передача аргументов командной строки исполняемой функции"""
    parsers = create_args()
    args = parsers.parse_args()
    create_issue(args)


if __name__ == '__main__':
    main()