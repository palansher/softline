# Базовый образ Python 3.11 (лёгкая версия slim)
FROM python:3.11-slim

# Установка рабочей директории внутри контейнера
WORKDIR /app

# Копирование файла зависимостей в контейнер
COPY requirements.txt .

# Установка Python зависимостей
# --no-cache-dir уменьшает размер образа
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всех файлов приложения в контейнер
COPY . .

# Открытие порта 5002 для data сервиса
EXPOSE 5002

# Переменная окружения для Flask (режим production)
ENV FLASK_ENV=production

# Команда запуска приложения
# gunicorn - производственный WSGI сервер
# --bind 0.0.0.0:5002 - слушать все интерфейсы на порту 5002
# app:app - модуль app, объект app
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "app:app"]