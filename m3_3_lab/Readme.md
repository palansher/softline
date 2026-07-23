# 3.3 Темы

видео от 2026.05.25

Код урока я повторял в папке m3_3_lesson

- [3.3 Темы](#33-темы)
  - [mvc 0:04](#mvc-004)
  - [pip 16:53](#pip-1653)
  - [Django 24:06](#django-2406)
    - [Установка 24:06](#установка-2406)
    - [Создание проекта 27:32](#создание-проекта-2732)
    - [manage.py 28:31](#managepy-2831)
    - [Создание модуля 29:20](#создание-модуля-2920)
    - [запуск проекта 34:43](#запуск-проекта-3443)
    - [Структура проекта 36:42](#структура-проекта-3642)
      - [wsgi.py](#wsgipy)
      - [settings.py 37:15](#settingspy-3715)
      - [urls.py 40:37](#urlspy-4037)
      - [](#)
    - [встроенная админка в Django 44:29](#встроенная-админка-в-django-4429)
    - [views.py 46:04](#viewspy-4604)
    - [запуск проекта 58:36](#запуск-проекта-5836)
  - [получаем get параметры 1:04:33](#получаем-get-параметры-10433)
  - [Как правильно делать токен csrfmiddlewaretoken для формы 2:03:19](#как-правильно-делать-токен-csrfmiddlewaretoken-для-формы-20319)
  - [Подготовка Django для обработки статики. 2:16:57](#подготовка-django-для-обработки-статики-21657)

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

```text
.  (Корневая папка, её можно переименовать)
└── lesson33
    ├── manage.py             <-- Главный пульт управления (запуск сервера, миграции)
    │
    ├── lesson33              <-- ПРОЕКТ (Настройки всего сайта)
    │   ├── __init__.py
    │   ├── settings.py       <-- Здесь мы регистрируем приложения
    │   ├── urls.py           <-- Главный навигатор (маршруты сайта)
    │   └── wsgi.py / asgi.py
    │
    └── my_app                <-- ПРИЛОЖЕНИЕ (Твой рабочий функционал)
        ├── apps.py           <-- Конфигурация самого приложения
        ├── models.py         <-- Здесь описываем таблицы для базы данных
        ├── views.py          <-- Здесь пишем логику (что делать, если пользователь зашел на страницу)
        ├── migrations/       <-- История изменений базы данных
        └── templates/        <-- Твои HTML-страницы
```

В экологии Django есть четкое разделение понятий Проект (Project) и Приложение (App).

Проект (Project) — это внутренний каталог lesson33. Это "мозг" и общая конфигурация твоего сайта. Он объединяет все настройки, базы данных и указывает, какие приложения должны работать вместе. Проект — это весь твой сайт целиком.

Приложение (App) — это папка my_app. Это изолированный, независимый кусочек функционала. Например, на сайте интернет-магазина my_app могло бы быть корзиной, блогом, системой отзывов или личным кабинетом.

С точки зрения самого языка Python: и внутренняя папка lesson33, и папка my_app являются модулями (пакетами), потому что внутри них Django создает файлы вроде __init__.py или apps.py, что позволяет Python импортировать код из одной папки в другую.

Важный следующий шаг
Так как ты только что создал приложение my_app, твой проект lesson33 о нем пока ничего не знает. Чтобы они подружились, тебе нужно сделать одно действие:

Открой файл lesson33/lesson33/settings.py, найди список INSTALLED_APPS и добавь туда свое приложение:

```Python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # ... другие стандартные приложения ...
    
    'my_app',  # <-- Добавь эту строчку
]
```

Теперь Django официально видит твое приложение, и ты можешь переходить к созданию первых страниц (View) и маршрутов (Url)!

settings.py и urls.py - основные файлы проекта. Отвечают за структуру проекта, они основные.

#### wsgi.py

— это, по сути, «дверь» для веб-сервера в твое Django-приложение.

Когда пользователь в браузере вводит адрес твоего сайта, этот запрос сначала попадает на полноценный веб-сервер (например, Nginx или Apache), который установлен на сервере (хостинге). Но Nginx сам по себе не умеет читать код на Python. Ему нужен посредник, который переведет запрос с языка веб-сервера на язык Python.

Этот стандарт-посредник и называется WSGI (Web Server Gateway Interface). А файл wsgi.py — это стандартный шлюз, который берет входящий запрос от веб-сервера и передает его внутрь Django, а потом возвращает ответ обратно.

Примечание: Когда ты запускаешь python manage.py runserver, Django включает свой простенький, встроенный сервер для разработки. Ему wsgi.py не нужен. Но как только ты решишь выложить сайт в интернет («в продакшн»), без wsgi.py ничего работать не будет.

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
