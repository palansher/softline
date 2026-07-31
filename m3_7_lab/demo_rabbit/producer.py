# отправляет данные в брокер

import os
from pathlib import Path

import pika
from dotenv import load_dotenv

# Явно находим корень проекта и .env файл
# (поднимись на нужное количество .parent в зависимости от структуры папок)
BASE_DIR = Path(__file__).resolve().parent  # Путь к корню с .env
env_path = BASE_DIR / ".env"

# Загружаем переменные из .env файла
print(f"Loading env from: {env_path}")
load_dotenv(dotenv_path=env_path)

# Считываем переменные окружения
RABBIT_USER = os.getenv("RABBITMQ_USER", "guest")
RABBIT_PASS = os.getenv("RABBITMQ_PASS", "guest")
RABBIT_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBIT_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))

if not RABBIT_USER or not RABBIT_PASS:
    raise ValueError(f"Не удалось загрузить RABBITMQ_USER/PASS из {env_path}")

# print(f"RabbitMQ credentials. RABBIT_USER: {RABBIT_USER}")

# Авторизация и подключение
credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
parameters = pika.ConnectionParameters(
    host=RABBIT_HOST, port=RABBIT_PORT, credentials=credentials
)

"""
Так как логин/пароль в .env изменились, RabbitMQ не обновит их в имеющемся volume автоматически.
Пересоздай контейнер и том:

docker compose down -v
docker compose up -d
"""


# BlockingConnection - это синхронное соединение
# ConnectionParameters - это параметры подключения

# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
connection = pika.BlockingConnection(parameters)

# Все операции с RabbitMQ через канал связи
# канал нужно активировать перед использованием

channel = connection.channel()

# Объявляем/регистрируем очередь
channel.queue_declare(queue="lesson7")

# по умолчанию exchange используется типа direct (exchange='')
# К нашему сообщению мы привязали ключ.
# channel.basic_publish(exchange="", routing_key="lesson7", body="Привет!")
channel.basic_publish(
    exchange="",
    routing_key="lesson7",
    body="Привет с метаданными!".encode(),
    properties=pika.BasicProperties(
        content_type="text/plain",
        delivery_mode=2,  # Сделать сообщение персистентным (сохранять на диск)
        headers={"source": "python-producer", "version": "1.0"},
    ),
)

# После этого сообщение публикуется.
# В случае проблем будет выброшено исключение Exception..


print("Сообщение успешно отправлено в Брокер")

connection.close()
