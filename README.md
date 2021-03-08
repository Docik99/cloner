Необходимо открыть терминал по адресу папки с проектом

#### Создание образа

`$ docker build -t cloner .`

#### Запуск образа

##### Получение списка пользователей
`$ docker run cloner -g https://gitwork.ru -t yhQvz2QsqXbxakY-zEqC`

##### Создание новых пользователей из данных, содержащихся в файле 
`$ docker run cloner -s http://localhost:10080 -t yhQvz2QsqXbxakY-zEqC -f out_of_users.json`

Где  **yhQvz2QsqXbxakY-zEqC** токен root пользователя, а **https://gitwork.ru** адрес хоста
##### Для запуска pylint

`$ pylint gitlab_user_sync.py`

##### Для запуска тестов

`$ nosetests --with-coverage --cover-package=gitlab_user_sync`