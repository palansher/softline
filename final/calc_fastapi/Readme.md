# Windows-style calculator на FastApi

## Отличия

см. [Windows-style calculator на Flask](../calc_flask/Readme.md)

Проект идентичен калькулятору на Flask, здесь используем FastAPI.

- В FastAPI для Jinja2Templates синтаксис функции url_for немного отличается от Flask: вместо filename= используется именованный аргумент path=

- В FastAPI тестировать API удобно с помощью штатного TestClient

## Структура проекта

```text
calculator_fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py              # Точка входа FastAPI (роуты, статика, шаблоны)
│   ├── core/
│   │   ├── __init__.py
│   │   └── calculator.py    # ООП логика (100% код из Flask-версии)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── payload.py       # Pydantic-модели для валидации DTO
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Без изменений
│   │   └── js/
│   │       └── app.js       # Без изменений
│   └── templates/
│       └── index.html       # HTML-шаблон (с адаптацией url_for для FastAPI)
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py   # Unit-тесты калькулятора
│   └── test_api.py          # Тесты API через FastAPI TestClient
├── run.py                   # Точка запуска Uvicorn
└── requirements.txt         # Зависимости
```

## Требования

Python 3.12

`pip install -r requirements.txt`

## Тесты

`PYTHONPATH=final/calc_fastapi pytest final/calc_fastapi`

## Запуск приложения

`python run.py`

http://127.0.0.1:8000/

## Swagger

- авто-документация Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
здесь можно изучить схему API и отправлять тестовые запросы прямо из браузера

- http://127.0.0.1:8000/openapi.json - спецификация OpenAPI (её сырой JSON)
