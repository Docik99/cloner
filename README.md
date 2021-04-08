Необходимо открыть терминал по адресу папки с проектом

#### Создание образа

`$ docker build -t cloner .`

#### Запуск образа

##### Получение списка пользователей
`$ docker run cloner gitlab_user_sync.py -g https://gitlab.ru -t yhQvz2QsqXbxakY-zEqC -f out_file`

out_file.json - файл, в котрый будут выведены данные пользователей (**-f** опциональный флаг)

##### Создание новых пользователей из данных, содержащихся в файле 
`$ docker run cloner gitlab_user_sync.py -s https://gitlab.ru-t yhQvz2QsqXbxakY-zEqC -f users-data`

users-data.json - файл, содержащий данные, необходимые для создания новых пользователей

##### Создание issue с новым паролем
`$ docker run cloner issue_create.py -s https://gitlab.ru -t yhQvz2QsqXbxakY-zEqC -f users-pass.json`

users-pass.json - файл содержаший пару логин-пароль

Где  **yhQvz2QsqXbxakY-zEqC** токен root пользователя, а **https://gitlab.ru** адрес хоста (**-g** и **-s** опциональные флаги, по умолчанию: https://gitwork.ru)
##### Для запуска pylint

`$ pylint gitlab_user_sync.py`

##### Для запуска тестов

`$ nosetests --with-coverage --cover-package=gitlab_user_sync`