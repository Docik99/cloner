Необходимо открыть терминал по адресу папки с проектом

#### Создание образа

`$ docker build -t cloner .`

#### Запуск образа

##### Получение списка пользователей
`$ docker run cloner gitlab_user_sync.py -g https://gitwork.ru -t yhQvz2QsqXbxakY-zEqC`

##### Создание новых пользователей из данных, содержащихся в файле 
`$ docker run cloner gitlab_user_sync.py -s https://gitwork.ru-t yhQvz2QsqXbxakY-zEqC -f out_of_users.json`

out_of_users.json - файл, в котрый будут выведены данные пользователей

##### Создание issue с новым паролем
`$ docker run cloner issue_create.py -s https://gitwork.ru -t yhQvz2QsqXbxakY-zEqC -f users-pass.json`

users-pass.json - файл содержаший пару логин-пароль

Где  **yhQvz2QsqXbxakY-zEqC** токен root пользователя, а **https://gitwork.ru** адрес хоста
##### Для запуска pylint

`$ pylint gitlab_user_sync.py`

##### Для запуска тестов

`$ nosetests --with-coverage --cover-package=gitlab_user_sync`