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
        response = requests.get(arg.serv + "/api/v4/users/" + str(
            todo['username']) + "/projects/?private_token=" + arg.token + "&simple=true")
        if response.status_code == 200:
            projects = json.loads(response.text)
            for project in projects:
                if project['name'] == 'timp':
                    print(project['id'])
        else:
            print(response.status_code)


def main():
    """Передача аргументов командной строки исполняемой функции"""
    parsers = create_args()
    args = parsers.parse_args()
    create_issue(args)


if __name__ == '__main__':
    main()
