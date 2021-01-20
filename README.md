Необходимо открыть терминал по адресу папки с проектом

#### Создание образа

`$ docker build -t cloner .`

#### Запуск образа

`$ docker run cloner -g hostname -t root-token`

Где **hostname** и **root-token** нужно заменить на необходимые значения

Примеры записи _hostname_: 

https://gitwork.ru

http://localhost:10080 

##### Для запуска pylint

`$ pylint gitlab_user_sync.py`