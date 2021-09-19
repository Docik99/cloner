Необходимо открыть терминал по адресу папки с проектом

## Создание образа

`$ docker build -t cloner .`

## Запуск образа

#### Получение списка пользователей
`$ docker run cloner gitlab_user_sync.py -f out_file g yhQvz2QsqXbxakY-zEqC`

    usage: gitlab_user_sync.py [-h] [-u URL] [-f FILE] operation token
    
    positional arguments:
      
      operation             input "g" for get users or "s" for create users
      
      token                 input root_token
    
    optional arguments:
      -h, --help            show this help message and exit
      -u URL, --url URL     input hostname (default https://gitwork.ru)
      -f FILE, --file FILE  input way to file (required flag if operation = s)
      
В качестве **operation** необходимо указать **g**

**yhQvz2QsqXbxakY-zEqC**  - токен root пользователя

out_file.json - файл, в котрый будут выведены данные пользователей (**-f** опциональный флаг)

#### Создание новых пользователей из данных, содержащихся в файле
`$ docker run cloner gitlab_user_sync.py -f users-data.json s yhQvz2QsqXbxakY-zEqC`

    usage: gitlab_user_sync.py [-h] [-u URL] [-f FILE] operation token
    
    positional arguments:
      
      operation             input "g" for get users or "s" for create users
      
      token                 input root_token
    
    optional arguments:
      -h, --help            show this help message and exit
      -u URL, --url URL     input hostname (default https://gitwork.ru)
      -f FILE, --file FILE  input way to file (required flag if operation = s)

В качестве **operation** необходимо указать **s**

users-data.json - файл, содержащий данные, необходимые для создания новых пользователей

#### Создание issue с новым паролем
`$ docker run cloner issue_create.py -u https://gitlab.ru yhQvz2QsqXbxakY-zEqC users-pass.json`

    usage: issue_create.py [-h] [-u URL] token file
    
    positional arguments:
      token              input root_token
      file               input way to file
    
    optional arguments:
      -h, --help         show this help message and exit
      -u URL, --url URL  input hostname (default "https://gitwork.ru")

users-pass.json - файл, содержаший пару логин-пароль

#### Корректировка email у пользователей
`$ docker run cloner email_correcter.py -u https://gitlab.ru yhQvz2QsqXbxakY-zEqC`

    usage: email_correcter.py [-h] [-u URL] token
    
    positional arguments:
      token              input root_token
    
    optional arguments:
      -h, --help         show this help message and exit
      -u URL, --url URL  input hostname (default "https://gitwork.ru")
      
В данный момент скрипт не способен менять email пользователей, в отличии от остальных данных.
Вероятнее всего это связано с багом https://gitlab.com/gitlab-org/gitlab/-/issues/25077
Проблему не удалось решить ни в 12 версии gitlab, ни в версии 14.0.10
      
#### Блокировка пользователей по списку
`$ docker run cloner locker.py -u https://gitlab.ru yhQvz2QsqXbxakY-zEqC file.json`

    usage: locker.py [-h] [-u URL] token file
    
    positional arguments:
      token              input root_token
      file               input way to file
    
    optional arguments:
      -h, --help         show this help message and exit
      -u URL, --url URL  input hostname (default "https://gitwork.ru")

file.json - файл с именами (name) пользователей, которых нужно заблокировать


#### Для запуска pylint
`$ pylint gitlab_user_sync.py`

`$ pylint email_correcter.py`

`$ pylint issue_create.py`

`$ pylint locker.py`

#### Для запуска тестов
`$ nosetests --with-coverage --cover-package=gitlab_user_sync`