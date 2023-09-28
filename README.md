# Spot

## Описание

Ценность приложения в  улучшении доступности, удобства и эффективности использования коворкинговых пространств для IT специалистов, а также улучшении управлении и оптимизации пространств для владельцев.

## Запуск проекта
* Создать виртуальное окружение и активировать его
* Установить зависимости 
```
python -m vevn venv
. venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

В папке ```api_spot ``` 
выполнить команды 
```
python manage.py createsuperuser
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Проект запустится на адресе http://http://127.0.0.1:8000/,
заполнить бд можно в админке (http://127.0.0.1:8000/admin/)
увидеть спецификацию API вы сможете по адресу http://127.0.0.1:8000/swagger-ui/
(на Windows не работает celery, это значит api запросы которые связаные с задачи будет очень долго выполняться)

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

- [![Python](https://img.shields.io/badge/-Python_3.11-464646?style=flat-square&logo=Python)](https://www.python.org/)
- [![Django](https://img.shields.io/badge/-Django_4.1-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
- celery
- redis

## Авторы:

**Изимов Арсений**  - https://github.com/Arseny13
