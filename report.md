**Отчёт о тестировании**

Участники:

Анастасия Калинина, группа 114

Панарин Родион, группа 109

**Отчёт**

Для запуска, выполним команду:

```docker compose up -d```

После чего запускаются все контейнеры, перечисленные в файле `docker-compose.yml`. Это можно проверить командой `docker ps`:

```
~ $ docker ps
CONTAINER ID   IMAGE           COMMAND                  CREATED         STATUS                    PORTS                                               NAMES
ee7b303ec185   nginx:alpine    "/docker-entrypoint.…"   5 minutes ago   Up 5 minutes              80/tcp, 0.0.0.0:4000->4000/tcp, :::4000->4000/tcp   mai_nosql-nginx-1
6c13fad1873b   otterchat_app   "python /home/otter/…"   5 minutes ago   Up 5 minutes              8000/tcp                                            mai_nosql-otterchat_app-1
7b1fc514183c   otterchat_app   "python /home/otter/…"   5 minutes ago   Up 5 minutes              8000/tcp                                            mai_nosql-otterchat_app-2
15138c3f2d8a   mongo           "docker-entrypoint.s…"   5 minutes ago   Up 5 minutes (healthy)    0.0.0.0:27018->27017/tcp, :::27018->27017/tcp       mai_nosql-mongo_db_node_02-1
3d273c86e148   mongo           "docker-entrypoint.s…"   5 minutes ago   Up 5 minutes (healthy)    0.0.0.0:27017->27017/tcp, :::27017->27017/tcp       mai_nosql-mongo_db_node_01-1
```

Для функционального тестирования выполним следующие HTTP-запросы к API:
1. Создадим пользователя:
```
curl --location '192.168.56.101:4000/user/originalusername' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "VeryUser",
    "email": "test@mail.mai"
}'
```
2. Затем, "войдём" от имени этого пользователя:
```
curl --location --request POST '192.168.56.101:4000/user/login/originalusername' \
--header 'Cookie: username=originalusername'
```
3. Создадим пост:
```
curl --location '192.168.56.101:4000/post/' \
--header 'Content-Type: application/json' \
--header 'Cookie: username=originalusername' \
--data '{
    "text": "my first post!"
}'
```
4. Получим список всех пользователей:
```
curl --location '192.168.56.101:4000/user' \
--header 'Cookie: username=originalusername'
```
Ответ API:
```
[
    {
        "username": "originalusername",
        "name": "VeryUser",
        "email": "test@mail.mai"
    }
]
```
5. Запросим список постов пользователя с ником `originalusername`:
```
curl --location '192.168.56.101:4000/post/originalusername' \
--header 'Cookie: username=originalusername'
```
Ответ API:
```
[
    {
        "author": "originalusername",
        "text": "my first post!",
        "sent_at": "2024-03-18T12:46:01.408000"
    }
]
```

Вывод: API работает и сохраняет новых пользователей, и сообщения от их лица, а также позволяет затем получить созранённую информацию. 

Проведём теперь тестирование на отказоустойчивость.

1. Для этого, отключим один из контейнеров API, тк их создано две реплики:

```
~ $ docker kill 6c13fad1873b
6c13fad1873b
```
Снова выполним запрос из пункта 5 функционального тестирования. Nginx задумывается на какое-то время, и, обнаружив, что первый контейнер API мёртв, перенаправляет на второй, и ответ совпадает с ожидаемым. 

2. Теперь проверим на отказоустойчивость саму БД. Для этого убьём первую ноду MongoDB:
```
~ $ docker kill 3d273c86e148
3d273c86e148
```
Поскольку данная нода контроллирует весь кластер, приложение теряет возможность общаться с базой, и больше не работает.

3. Добавим ещё одну ноду в MongoDB, и запустим проект заново:
```
docker compose down && docker compose up -d
```  
Посмотрим запущенные контейнеры:
```
$ docker ps
CONTAINER ID   IMAGE           COMMAND                  CREATED              STATUS                        PORTS                                               NAMES
d84159ba296f   nginx:alpine    "/docker-entrypoint.…"   About a minute ago   Up About a minute             80/tcp, 0.0.0.0:4000->4000/tcp, :::4000->4000/tcp   mai_nosql-nginx-1
5adb467f9e41   otterchat_app   "python /home/otter/…"   About a minute ago   Up About a minute             8000/tcp                                            mai_nosql-otterchat_app-2
0f7b05d26059   otterchat_app   "python /home/otter/…"   About a minute ago   Up About a minute             8000/tcp                                            mai_nosql-otterchat_app-1
d66fe6df0477   mongo           "docker-entrypoint.s…"   About a minute ago   Up About a minute (healthy)   0.0.0.0:27018->27017/tcp, :::27018->27017/tcp       mai_nosql-mongo_db_node_02-1
7637efa0331c   mongo           "docker-entrypoint.s…"   About a minute ago   Up About a minute (healthy)   0.0.0.0:27019->27017/tcp, :::27019->27017/tcp       mai_nosql-mongo_db_node_03-1
6be5005923ea   mongo           "docker-entrypoint.s…"   About a minute ago   Up About a minute (healthy)   0.0.0.0:27017->27017/tcp, :::27017->27017/tcp       mai_nosql-mongo_db_node_01-1
```
А теперь убьём третью ноду!
```
docker kill 7637efa0331c
```
Проверим работоспособность запросами на чтение и запись. Приложение продолжает работать успешно в обоих случаях.

Убьём ещё одну:
```
docker kill d66fe6df0477
```
После этого работать с приложением становится невозможным.

**Выводы**

В рамках данного курса участники команды ознакомились с распределёнными технологиями и их применением для разработки приложений, способных к отказоустойчивости в условиях высокой нагрузки и отключения одного из услов.