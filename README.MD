Приложение билдится с помощью docker-compose с использованием *compose.yaml* файла.
Команда: *docker-compose -f ./compose.yaml up -d --build*

Предварительно необходимо скопировать *dist.env* файл с названием *.env*
После необходимо выполнить миграции командой *alembic upgrade head* в контейнере api

Запросы принимаются на **localhost:80**. На **localhost:80/docs** хранится документация по всем методам апи

Выполните команду *pytest --cov* в контейнере api для запуска тестов

![image](/tests_result.png)