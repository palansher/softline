import configparser
import logging

from confluent_kafka import Consumer, KafkaError, KafkaException

logging.basicConfig(
    level=logging.INFO, format="{asctime} - {name} {levelname} {message}", style="{"
)

# Создаем логгер для текущего модуля
logger = logging.getLogger(__name__)


def main():
    config = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "my_group",  # для распределения нагрузки между несколькими консьюмерами. Обязательно для консюмера.
        "auto.offset.reset": "earliest",  # Стратегия при отстутсвии сохраненного offset:
        # 1) earliest: читаем с самого начала топика
        # 2) latest: читаем только новые соообщения. Забываем, что было раньше.
        # 2) none: завершаем работу ошибкой
        "enable.auto.commit": True,  # включение автоматического подтверждения обработки сообщения. Обязательно для консюмеров.
    }

    consumer = Consumer(config)
    topic = "my_topic"

    try:
        # Подписываемся на топик или группу топиков
        consumer.subscribe([topic])
        logger.info(f"Успешная подписка на топик {topic}")

        # Бесконечный цикл для обработки сообщений
        while True:
            msg = consumer.poll(1.0)  # проверяем наличие новых сообщений каждую секунду
            if msg is None:
                continue # Если сообщений нет, то пропускаем.
            if msg.error():
                logger.error(f"Ошибка при получении сообщения (poll): {msg.error()}")
                continue # Пропускаем, если нет ошибок
            try:
                key = msg.key().decode("utf8") if msg.key() else None
                value = msg.value().decode("utf8") if msg.value() else None
                logger.info(
                    f"Получено: topic: %s, partition: %s, offset: %s, key:%s, value: %s",
                    topic,
                    msg.partition(),
                    msg.offset(),
                    key,
                    value,
                )
            except (KafkaException, KafkaError) as e:
                logger.error(f" Ошибка при получении ключа и значения из сообщения: {e}")
    except Exception as e:
        logger.error("Критическая ошибка", e)
    except KeyboardInterrupt:
        logger.error("Прервано пользователем")
    finally:
        consumer.close()
        logger.info("Консьюмер закрыт!")


if __name__ == "__main__":
    main()
