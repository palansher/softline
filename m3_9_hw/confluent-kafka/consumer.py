"""Основной модуль чтения сообщений из Apache Kafka."""

import logging
import signal
from typing import Any

from car import Car
from car_deserializer import CarDeserializer
from consumer_config import ConsumerConfig
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from key_deserializer import KeyDeserializer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

MAX_MESSAGES = 10


class KafkaConsumerApp:
    """Приложение для чтения и обработки событий Car из Kafka."""

    def __init__(self, config: ConsumerConfig | None = None) -> None:
        self.config = config or ConsumerConfig()
        self.key_deserializer = KeyDeserializer()
        self.value_deserializer = CarDeserializer()
        self.consumer: KafkaConsumer | None = None
        self._running = True

    def _setup_signal_handlers(self) -> None:
        """Настройка обработчиков сигналов для корректного завершения (Graceful Shutdown).

        ПРОДАКШЕН-ПРАКТИКА:
        При остановке контейнера в Docker / K8s отправляется сигнал SIGTERM (или SIGINT при Ctrl+C).
        Перехватываем их, чтобы плавно завершить цикл и отправить LeaveGroup в Kafka.
        """

        def handle_signal(sig: int, _frame: Any) -> None:
            logger.info("Получен сигнал остановки (%s). Завершение работы...", sig)
            self._running = False

        signal.signal(signal.SIGINT, handle_signal)
        signal.signal(signal.SIGTERM, handle_signal)

    def run(self) -> None:
        """Основной цикл чтения сообщений из Kafka."""
        self._setup_signal_handlers()

        try:
            self.consumer = KafkaConsumer(
                self.config.topic,
                **self.config.get_consumer_config(),
                key_deserializer=self.key_deserializer,
                value_deserializer=self.value_deserializer,
                # КРИТИЧЕСКИ ВАЖНО ДЛЯ GRACEFUL SHUTDOWN:
                # По умолчанию итератор `for message in consumer` блокирует поток навсегда.
                # `consumer_timeout_ms=1000` заставляет итератор раз в 1 секунду прерываться,
                # давая возможность циклу `while self._running` проверить флаг остановки!
                consumer_timeout_ms=1000,
            )

            # ПРИМЕЧАНИЕ ПО ЛОГАМ: При первом запуске здесь возможна ошибка:
            # [WARNING] kafka.coordinator: Marking the coordinator dead... [Error 16] NotCoordinatorForGroupError
            # Это штатное поведение Kafka! Координатор группы еще инициализируется
            # или выбирается кластером. Библиотека сама повторит запрос через пару мс.
            logger.info("Kafka Consumer успешно запущен. Ожидание сообщений...")
            messages_received = 0

            while self._running:
                for message in self.consumer:
                    if not self._running:
                        break

                    car: Car | None = message.value
                    key: str | None = message.key

                    if car is None:
                        logger.warning(
                            "Получено пустое сообщение (tombstone) или не удалось десериализовать. Offset: %d",
                            message.offset,
                        )
                        continue

                    messages_received += 1

                    logger.info(
                        # Через стандартное представление dataclass (__repr__)
                        "Сообщение #%d | Partition: %d | Offset: %d | Key: %s | Car: %s",
                        messages_received,
                        message.partition,
                        message.offset,
                        key,
                        car,  # Выведет: Car(id=1, brand=CarBrand(id=10, name='Toyota'), model='Camry', ...)
                    )

                    if messages_received >= MAX_MESSAGES:
                        logger.info(
                            "Достигнут лимит сообщений (%d). Завершение работы.", MAX_MESSAGES
                        )
                        self._running = False
                        break

            if messages_received == 0 and self._running:
                logger.warning("Сообщения не получены за время ожидания.")

        except KafkaError as err:
            logger.error("Ошибка уровня Kafka: %s", err)
        except Exception as err:
            logger.exception("Непредвиденная ошибка в работе Consumer: %s", err)
        finally:
            # КРИТИЧЕСКИ ВАЖНО:
            # Метод close() явно отправляет координатору брокера сообщение `LeaveGroup`.
            # В результате кластер мгновенно перераспределяет партиции на другие сервисы,
            # не дожидаясь истечения session_timeout_ms (30 секунд).
            if self.consumer is not None:
                self.consumer.close()
                logger.info("Kafka Consumer закрыт.")


if __name__ == "__main__":
    app = KafkaConsumerApp()
    app.run()
