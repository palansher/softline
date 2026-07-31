# получаем данные из брокера

import os
from pathlib import Path

import pika
from dotenv import load_dotenv

# from pika import callback

# Явно находим корень проекта и .env файл
# (поднимись на нужное количество .parent в зависимости от структуры папок)
BASE_DIR = Path(__file__).resolve().parent  # Путь к корню с .env
env_path = BASE_DIR / ".env"

# Загружаем переменные из .env файла
print(f"Loading env from: {env_path}")
load_dotenv(env_path)

# Считываем переменные окружения
RABBIT_USER = os.getenv("RABBITMQ_USER", "guest")
RABBIT_PASS = os.getenv("RABBITMQ_PASS", "guest")
RABBIT_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBIT_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))

if not RABBIT_USER or not RABBIT_PASS:
    raise ValueError(f"Не удалось загрузить RABBITMQ_USER/PASS из {env_path}")


# Авторизация и подключение
credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
parameters = pika.ConnectionParameters(
    host=RABBIT_HOST, port=RABBIT_PORT, credentials=credentials
)


# connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
connection = pika.BlockingConnection(parameters)


channel = connection.channel()

# из какой очереди будем доставать наши сообщения
# Пока просто объявили эту очередь.
channel.queue_declare(queue="lesson7")

"""
Функция запускается при получении сообщения нашим брокером (по событию on_message_callback).
"""

# def callback(ch, method, props, body):
#     print(f"Сообщение {body.decode()} получено!")


def callback(ch, method, properties, body):
    # 1. Декодируем тело сообщения (из bytes в str)
    try:
        payload = body.decode("utf-8")
    except UnicodeDecodeError:
        payload = str(body)

    print("\n" + "=" * 50)
    print("📩 ПОЛУЧЕНО НОВОЕ СООБЩЕНИЕ")
    print("=" * 50)

    # 2. Информация о доставке из `method`
    print("📌 МЕТАДАННЫЕ ДОСТАВКИ (method):")
    print(f"  • Consumer Tag : {method.consumer_tag}")
    print(f"  • Delivery Tag  : {method.delivery_tag} (порядковый номер в канале)")
    print(
        f"  • Redelivered   : {method.redelivered} (было ли переотправлено повторно?)"
    )
    print(f"  • Exchange      : '{method.exchange}'")
    print(f"  • Routing Key   : '{method.routing_key}'")

    # 3. Свойства сообщения из `properties`
    print("\n⚙️ СВОЙСТВА СООБЩЕНИЯ (properties):")
    # pika предоставляет метод slots() или атрибут _slots для получения списка бизнес-свойств
    props_dict = {
        prop: getattr(properties, prop)
        for prop in properties.__slots__
        if getattr(properties, prop) is not None
    }

    if props_dict:
        for key, val in props_dict.items():
            print(f"  • {key}: {val}")
    else:
        print("  • (Свойства не заданы — используются дефолтные)")

    if props_dict:
        for key, val in props_dict.items():
            print(f"  • {key}: {val}")
    else:
        print("  • (Свойства не заданы / используем дефолтные)")

    # 4. Информация о канале из `ch`
    print("\n🔌 ИНФОРМАЦИЯ О КАНАЛЕ (ch):")
    print(f"  • Channel Number : {ch.channel_number}")
    print(f"  • Is Open        : {ch.is_open}")

    # 5. Содержимое тела сообщения
    print("\n📦 ТЕЛО СООБЩЕНИЯ (body):")
    print(f"  • Raw Bytes      : {body}")
    print(f"  • Decoded Text   : {payload}")
    print("=" * 50 + "\n")


"""
auto_ack=True автоматическое подтверждение получения сообщения.
Как только запустится callback, мы считаем, что сообщение доставлено.
Тогда брокер увидит, что сообщение получено и удалит это сообщение.

"""

# Подписываем получателя к этой очереди
channel.basic_consume(queue="lesson7", on_message_callback=callback, auto_ack=True)

try:
    # включаем бесконечный цикл ожидания сообщений из брокер
    # Consumer всегда активен, ждет сообщений.
    channel.start_consuming()
except KeyboardInterrupt:
    # Разрываем соединение консьюмера с брокера по нажатию клавиши CTRL + C
    connection.close()
