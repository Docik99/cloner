Необходимо открыть терминал по адресу папки с проектом

#### Создание образа

`$ docker build -t cloner .`

#### Запуск образа

`$ docker run cloner -g https://gitwork.ru -t yhQvz2QsqXbxakY-zEqC`

Где  **yhQvz2QsqXbxakY-zEqC** токен root пользователя, а **https://gitwork.ru** адрес хоста
##### Для запуска pylint

`$ pylint gitlab_user_sync.py`