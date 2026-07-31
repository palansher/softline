import logging

from confluent_kafka import Consumer, KafkaException

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
        # 3) none: завершаем работу ошибкой
        "enable.auto.commit": True,  # включение автоматического подтверждения обработки сообщения. Обязательно для консюмеров.
    }

    consumer = Consumer(config)
    topic = "my_topic"

    try:
        # Подписываемся на топик или группу топиков
        consumer.subscribe([topic])
        logger.info("Успешная подписка на топик %s", topic)

        # Бесконечный цикл для обработки сообщений
        while True:
            msg = consumer.poll(1.0)  # проверяем наличие новых сообщений каждую секунду
            if msg is None:
                continue  # Если сообщений нет, то пропускаем.
            if msg.error():
                logger.error("Ошибка при получении сообщения (poll): %s", msg.error())
                continue  # Пропускаем, если нет ошибок
            try:
                
                """
                "decode" is not a known attribute of "None" Pylance (reportOptionalMemberAccess)
                
                Эта ошибка возникает из-за особенностей работы анализатора типов (Type Checker) в Pylance.

                Когда мы пишем msg.key().decode(...) if msg.key() is not None else None, Pylance делает два отдельных вызова метода msg.key().
                Тайпчекер не может гарантировать, что вызов метода дважды подряд вернёт одно и то же значение,
                поэтому он не делает сужение типов (Type Narrowing) для первого вызова и продолжает считать, что msg.key() может вернуть None.
                
                Решение
                Нужно сохранить результат msg.key() и msg.value() в промежуточные переменные.
                Тогда Pylance поймет, что после проверки if raw_key is not None переменная гарантированно имеет тип bytes:
                """                
                raw_key = msg.key()
                raw_value = msg.value()

                key = raw_key.decode("utf-8") if raw_key is not None else None
                value = raw_value.decode("utf-8") if raw_value is not None else None

                logger.info(
                    "Получено: topic: %s, partition: %s, offset: %s, key:%s, value: %s",
                    topic,
                    msg.partition(),
                    msg.offset(),
                    key,
                    value,
                )
            except (KafkaException, UnicodeDecodeError) as e:
                logger.error(" Ошибка при получении ключа и значения из сообщения: %s", e)
    except KeyboardInterrupt:
        logger.error("Прервано пользователем")
    except Exception as e:  # noqa: BLE001
        logger.error("Критическая ошибка: %s", e)
    finally:
        consumer.close()
        logger.info("Консьюмер закрыт!")


if __name__ == "__main__":
    main()
