# Spot

[![api_spot](https://github.com/ZUS666/spot/actions/workflows/api_spot.yml/badge.svg)](https://github.com/ZUS666/spot/actions/workflows/api_spot.yml)

## Описание

Ценность приложения в  улучшении доступности, удобства и эффективности использования коворкинговых пространств для IT специалистов, а также улучшении управлении и оптимизации пространств для владельцев.

Бэкенд веб-сервиса для поиска веб-сервиса "Онлайн-бронирование в коворкингах для IT специалистов". Возможности: Все пользователи:

* Аутентификация (TokenAuthentication);
* Просмотр, поиск, фильтрация всех локаций;
* Просмотр ивентов, правил и вопросов сайта;

Клиенты:

* Личный кабинет с возможностью изменить данные в профиле;
* Список забонированых мест;
* Добавление локации в избранное и удаление из избранного;
* Бронь мест в локации и отмена записи (из ЛК);

Реализаново 4 приложение:
* api: приложение связанное с запросами (api);
* spots: основный модели( локации, заказы, споты и тд);
* users: модель пользователя;
* information: модели вопросов, ивентов, правил;

## API-документация:

http://spotit.acceleratorpracticum.ru/api/docs/


## Запуск проекта
* Установите docker
* Для установки на ubuntu выполните следующие команды:
```
sudo apt install docker
```
Про установку на других операционных системах вы можете прочитать в [документации](https://docs.docker.com/engine/install/)

* Склонируйте репозиторий на локальную машину:
```
git clone git@github.com:ZUS666/spot.git
```
* В корне проекта создайте .env файл по аналогии с файлом .env.example.
* Перейдите в папку infra и соберите контейнеры:
```
docker compose up -d
```
* Примените миграции:
```
docker compose exec web python manage.py migrate
```
* Создайте суперпользователя Django:
```
docker compose exec web python manage.py createsuperuser
```
* Соберите статику:
```
docker compose exec web python manage.py collectstatic --noinput
```

* Для заполнения или обновления базы данных перейдите по адресу https://localhost/admin
* Для получения документация по api перейдите по адресу https://localhost/api/docs/


## Запуск проекта на локальной машине Linux

* Создать виртуальное окружение и активировать его
* Установить зависимости 
```
sudo apt install python3.10-venv
python3 -m vevn venv
source venv/bin/activate
pip install -r requirements.txt
```

* Установите Redis в качестве брокера Celery и серверной части базы данных
```
sudo apt update
sudo apt install redis
```
* Запустить сервер терминале `redis-server`
* В другом терминале(2) перейти в папку `api_spot` и запустить celery
```
cd api_spot
python -m celery -A api_spot worker
```
* В первом терминале запустить сервер Django + cделать миграции
```
python manage.py createsuperuser
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Так же можно запустить flower(для мониторинга задач) в третим терминале.
```
celery -A api_spot flower --port=5001
```

* Для заполнения или обновления базы данных исползовать https://localhost/admin 
* в Postman тестировать api


## Используемые технологии

- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
- ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
- ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
- ![Celery](https://a11ybadges.com/badge?logo=celery)
- ![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
- ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
- flower

## Авторы:

- **Тагиров Руслан**  - https://github.com/ZUS666
- **Изимов Арсений**  - https://github.com/Arseny13
