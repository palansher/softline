from confluent_kafka import Producer

import logging
import socket

# Настройка форматирования логов с временем, именем логгера

logging.basicConfig(level=logging.INFO,
                    format='{asctime} - {name} {levelname} {message}',
                    style='{')

# Создаем логгер для текущего модуля
logger = logging.getLogger(__name__)

# Конфигурация для продюсера

KAFKA_CONFIG = {
    'bootstrap.servers': 'localhost:9092',
    'client.id':socket.gethostname(), #идентификатор клиента(имя хоста)
    'message.timeout.ms': 5000, #таймаут отправки сообщения в миллисекундах
    'socket.keepalive.enable': True, #включаем поддержку keep-alive для сокета
    'enable.idempotence': False, #отключили идемпонтентность для упрощения отладки
}

TOPIC = 'my_topic'
MAX_MESSAGES = 10 #КОЛИЧЕСТВО СООБЩЕНИЙ ДЛЯ ОТПРАВКИ

def delivery_report(err, msg):
    """Callback-функция, вызываемая при подтверждении доставки сообщения
    Args:
        err: Ошибка доставки (None если успешно)
        msg: Объект с сообщением + метаданные
    """
    if err is not None:
        logger.error(err)
    else:
        logger.info(f'Сообщение отправлено: topic={msg.topic()}'
                    f'Партиция: {msg.partition()},'
                    f'Offset: {msg.offset()},'
                    f'Key: {msg.key()},'
                    f' msg={msg.value()}')

def main():
    producer = Producer(KAFKA_CONFIG)
    try:
        # Тест подключения к Кафка. Запрос метаданных от кластера
        # producer.list_topics(timeout=10)
        # logger.info("Успешное подключение к Kafka")

        for i in range(MAX_MESSAGES):
            key = f'key-{i}'
            value = f'value-{i}'

            # Асинхронная отправка сообщений в Кафка

            producer.produce(topic=TOPIC, key=key.encode('utf-8'), value=value.encode('utf-8'),
                             callback=delivery_report) #callback для обработки результата

            producer.poll(0) #неблокирующий poll
        producer.flush(timeout=10)
        logger.info("Отправка завершена")
    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    main()