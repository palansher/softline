"""Основной модуль отправки сообщений в Apache Kafka."""

import logging
from datetime import datetime
from typing import Any

# from car import Car
from car_creater import generate_random_car
from kafka import KafkaProducer
from kafka.errors import KafkaError
from key_serializer import KeySerializer
from producer_config import ProducerConfig
from serializer import ObjSerializer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

MAX_MESSAGES = 10


class KafkaProducerApp:
    """Приложение для генерации и отправки событий Car в Kafka."""

    def __init__(self, config: ProducerConfig | None = None) -> None:
        self.config = config or ProducerConfig()
        self.value_serializer = ObjSerializer()
        self.key_serializer = KeySerializer()
        self.producer: KafkaProducer | None = None

    def _on_send_success(self, record_metadata: Any) -> None:
        """Callback при успешной подтвержденной доставке сообщения в Kafka."""
        logger.info(
            "Сообщение доставлено в топик '%s' [партиция %d, оффсет %d]",
            record_metadata.topic,
            record_metadata.partition,
            record_metadata.offset,
        )

    def _on_send_error(self, exc: Exception) -> None:
        """Callback при неисправимой ошибке отправки сообщения."""
        logger.error("Ошибка при отправке сообщения в Kafka: %s", exc, exc_info=True)

    def run(self) -> None:
        """Основной цикл отправки сообщений."""
        try:
            self.producer = KafkaProducer(
                **self.config.get_producer_config(),
                key_serializer=self.key_serializer,
                value_serializer=self.value_serializer,
            )

            for i in range(MAX_MESSAGES):
                car = generate_random_car()
                logger.info("Подготовка к отправке сообщения #%d (ID: %s)", i, car.id)

                # ПРОДАКШЕН-ПРАКТИКА: Распределение по партициям.
                # Мы передаем `key=car.id`, но НЕ передаем жесткий `partition`.
                # Kafka автоматически применит хэширование (Murmur2) к ключу:
                # `partition = hash(key) % total_partitions`.
                # Это гарантирует, что события с одинаковым key попадут в одну партицию.
                send_kwargs: dict[str, Any] = {
                    "topic": self.config.topic,
                    "timestamp_ms": int(datetime.now().timestamp() * 1000),
                    "key": car.id,
                    "value": car,
                }
                if self.config.partition is not None:
                    send_kwargs["partition"] = self.config.partition

                # Вызов send() НЕ отправляет сообщение сразу в сеть!
                # Он кладет его в локальный батч-буфер и возвращает Future.
                future = self.producer.send(**send_kwargs)

                # Асинхронная обработка результатов через колбэки
                future.add_callback(self._on_send_success).add_errback(self._on_send_error)

            logger.info(
                "Сброс буфера (flush) и ожидание доставки всех %d сообщений...", MAX_MESSAGES
            )
            # ПРОДАКШЕН-ПРАКТИКА: flush() принудительно отправляет все накопленные батчи
            # из памяти на брокер и блокирует поток до получения ответов (acks).
            self.producer.flush()
            logger.info("Все %d сообщений успешно обработаны.", MAX_MESSAGES)

        except KafkaError as err:
            logger.error("Ошибка уровня Kafka: %s", err)
        except Exception as err:
            logger.exception("Непредвиденная ошибка в работе Producer: %s", err)
        finally:
            # ПРОДАКШЕН-ПРАКТИКА: Гарантированное освобождение ресурсов и закрытие сокетов.
            if self.producer is not None:
                self.producer.close()
                logger.info("Kafka Producer закрыт.")


if __name__ == "__main__":
    app = KafkaProducerApp()
    app.run()
