Необходимо открыть терминал по адресу папки с проектом

#### Создание образа

`$ docker build -t cloner .`

#### Запуск образа

##### Получение списка пользователей
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

out_file.json - файл, в котрый будут выведены данные пользователей (**-f** опциональный флаг)

##### Создание новых пользователей из данных, содержащихся в файле 
`$ docker run cloner gitlab_user_sync.py -f users-data s yhQvz2QsqXbxakY-zEqC`

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

##### Создание issue с новым паролем
`$ docker run cloner issue_create.py -u https://gitlab.ru -t yhQvz2QsqXbxakY-zEqC -f users-pass.json`

Флаги:

-u (--url) Адрес хоста, к которому необходимо подключиться

-t (--token) Позволяет передать token пользователя, от чьего имени выполняются действия

-f (--file) Позволяет указать путь к файлу

users-pass.json - файл, содержаший пару логин-пароль

Где  **yhQvz2QsqXbxakY-zEqC** токен root пользователя, а **https://gitlab.ru** адрес хоста (**-g** и **-s** опциональные флаги, по умолчанию: https://gitwork.ru)
##### Для запуска pylint

`$ pylint gitlab_user_sync.py`

##### Для запуска тестов

`$ nosetests --with-coverage --cover-package=gitlab_user_sync`