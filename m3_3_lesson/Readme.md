# 3.3 Темы

видео от 2026.05.25

Код урока я повторял в папке m3_3_lesson

## mvc 0:04

## pip 16:53

## Django 24:06

### Установка 24:06

`python -m pip install Django`

### Создание проекта 27:32

`django-admin startproject lesson33`

Почему-то создает две вложенные папки с одинаковым именем проекта lesson33/lesson33

### manage.py 28:31

файлик для установки модулей и запуска сервера,
обычно никогда не трогаем, он служебный.

### Создание модуля 29:20

`python manage.py startapp my_app`

Запускать эту команду нужно там, где есть файл manage.py

### запуск проекта 34:43

`python manage.py runserver [port 8081 опционально]`

открываем предложенный сайт и видим ракету

Запускать эту команду нужно там, где есть файл manage.py

### Структура проекта 36:42

wsgi.py для запуска нашего приложения

settings.py и urls.py - основные файлы проекта. Отвечают за структуру проекта, они основные.

#### settings.py 37:15

INSTALLED_APPS 37:58

регистрируем здесь модули

зарегистрировали наш модуль my_app в INSTALLED_APPS 38:19

TEMPLATES 39:07 путь к шаблонам / вьюшкам

DATABASES 40:00 настройки базы данных

STATIC_URL Где должны находиться статические картинки, CSS и прочее.

#### urls.py 40:37

####

### встроенная админка в Django 44:29

http://127.0.0.1:8000/admin

(.venv) ✔ ~/code/learn-python/m3_3_lab/lesson33 [main|✚ 2…2]
07:58 $ python manage.py migrate

```bash

# в папке где manage.py

# If you are trying to run for the first time then first do
python manage.py migrate
# this will migrate all the data into migrate folder

# then simply run

python manage.py createsuperuser
Username (leave blank to use 'vp'): vp
Email address: palansher@outlook.com
Password: qwerty
Password (again):
This password is too short. It must contain at least 8 characters.
This password is too common.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.

```

apps.py заполняется автоматически. 45:34

models.py описывает структуру таблиц в базе данных

tests.py для unit тестеров

### views.py 46:04

Вьюшки, они же контроллеры -  запускают функции по запросу

заполняем views.py 49:07

53:29 пример создания Django проекта в PyCharm Professional

### запуск проекта 58:36

python manage.py runserver

## получаем get параметры 1:04:33

## Как правильно делать токен csrfmiddlewaretoken для формы 2:03:19

```JavaScript
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
```

## Подготовка Django для обработки статики. 2:16:57
