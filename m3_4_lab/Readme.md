# Особенности вебинара 3.4

запись от 28.05.2026

## Начало Django 09:54

## 10:30 работа со статикой шаг 1

## 12:49 работа со статикой шаг 2

В шаблоне необходимо активировать статик.
В шаблоне, где используем статические данные:
{% load static %}

## 13:34 подключение статических файлов

## 0:17:59 передача данных шаблон, обход списка и обход списка словарей

## создание каталога товаров 0:31:23

## базы, начало 0:59:43

### подключение и создание базы 1:03:24

```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": 'm3_4_lab',
        "USER": 'postgres',
        "PASSWORD": 'admin',
        "HOST": 'localhost',
        "PORT": 5432
    }
}

```

### наполнение базы 1:07:30

m3_4_lab/.infra/db/postgres-db-init/init-scripts/create-structure.sql

### RETURNING 1:13:38

## начало ORM 1:14:22

Создаем модель с описанием структуры таблицы в model.py

```
class Car(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
```

### Миграции

#### определение 1:18:30

#### собственно миграции

`pip install psycopg2-binary`

На основе модели необходимо создать миграцию. Миграции нужны, чтобы на основе модели была создана таблица.
Для создания миграции используем команду в папке проекта  где manage.py:

```bash
python manage.py makemigrations

# Migrations for 'my_app':
#   my_app/migrations/0001_initial.py
#     + Create model Car
```

После команды выше будет создан файл с миграцией в ` m3_4_lab/my_app/migrations/0001_initial.py`.

Чтобы этот файл запустить и на его основе создать таблицу

используем команду

`python manage.py migrate`

В базе создастся таблица my_app_car по имени модуля "my_app" + имени модели 'Car'.

1:30:12 после перерыва. продолжение.
