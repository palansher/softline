"""Основной модуль чтения сообщений из Apache Kafka (confluent-kafka)."""

import logging
import signal
from typing import Any

from car import Car
from car_deserializer import CarDeserializer
from confluent_kafka import Consumer, KafkaError
from consumer_config import ConsumerConfig
from key_deserializer import KeyDeserializer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

MAX_MESSAGES = 10


class KafkaConsumerApp:
    """Приложение для чтения и обработки событий Car из Kafka с помощью confluent-kafka."""

    def __init__(self, config: ConsumerConfig | None = None) -> None:
        self.config = config or ConsumerConfig()
        self.key_deserializer = KeyDeserializer()
        self.value_deserializer = CarDeserializer()
        self.consumer: Consumer | None = None
        self._running = True

    def _setup_signal_handlers(self) -> None:
        """Настройка обработчиков сигналов Graceful Shutdown."""

        def handle_signal(sig: int, _frame: Any) -> None:
            logger.info("Получен сигнал остановки (%s). Завершение работы...", sig)
            self._running = False

        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)

    def run(self) -> None:
        """Основной цикл чтения сообщений из Kafka."""
        self._setup_signal_handlers()

        try:
            self.consumer = Consumer(self.config.get_consumer_config())
            self.consumer.subscribe([self.config.topic])

            logger.info("Kafka Consumer успешно запущен. Ожидание сообщений...")
            messages_received = 0

            while self._running:
                # poll(timeout=1.0) заменяет consumer_timeout_ms.
                # Блокирует поток на 1 секунду в ожидании нового сообщения.
                msg = self.consumer.poll(timeout=1.0)

                if msg is None:
                    continue

                err = msg.error()
                if err is not None:
                    # Игнорируем техническое событие достижения конца партиции
                    if err.code() == KafkaError._PARTITION_EOF:
                        continue
                    logger.error("Ошибка уровня Kafka: %s", err)
                    break

                key = self.key_deserializer(msg.key())
                car: Car | None = self.value_deserializer(msg.value())

                if car is None:
                    logger.warning(
                        "Получено пустое сообщение (tombstone) или не удалось десериализовать. Offset: %d",
                        msg.offset(),
                    )
                    continue

                messages_received += 1

                logger.info(
                    "Сообщение #%d | Partition: %d | Offset: %d | Key: %s | Car: %s",
                    messages_received,
                    msg.partition(),
                    msg.offset(),
                    key,
                    car,
                )

                if messages_received >= MAX_MESSAGES:
                    logger.info("Достигнут лимит сообщений (%d). Завершение работы.", MAX_MESSAGES)
                    self._running = False

            if messages_received == 0 and self._running:
                logger.warning("Сообщения не получены за время ожидания.")

        except Exception as err:
            logger.exception("Непредвиденная ошибка в работе Consumer: %s", err)
        finally:
            if self.consumer is not None:
                # Метод close() бережно коммитит оффсеты и отправляет LeaveGroup в координатор
                self.consumer.close()
                logger.info("Kafka Consumer закрыт.")


if __name__ == "__main__":
    app = KafkaConsumerApp()
    app.run()
