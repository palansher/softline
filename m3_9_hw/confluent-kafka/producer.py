"""Основной модуль отправки сообщений в Apache Kafka (confluent-kafka)."""

import logging
from typing import Any

from car_creater import generate_random_car
from confluent_kafka import Producer
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
    """Приложение для генерации и отправки событий Car в Kafka с помощью confluent-kafka."""

    def __init__(self, config: ProducerConfig | None = None) -> None:
        self.config = config or ProducerConfig()
        self.value_serializer = ObjSerializer()
        self.key_serializer = KeySerializer()
        self.producer: Producer | None = None

    def _delivery_report(self, err: Any, msg: Any) -> None:
        """Callback доставки сообщения на брокер.

        В confluent-kafka передаются 2 аргумента: err (ошибка) и msg (объект Message).
        """
        if err is not None:
            logger.error("Ошибка при отправке сообщения в Kafka: %s", err)
        else:
            logger.info(
                "Сообщение доставлено в топик '%s' [партиция %d, оффсет %d]",
                msg.topic(),
                msg.partition(),
                msg.offset(),
            )

    def run(self) -> None:
        """Основной цикл отправки сообщений."""
        try:
            self.producer = Producer(self.config.get_producer_config())

            for i in range(MAX_MESSAGES):
                car = generate_random_car()
                logger.info("Подготовка к отправке сообщения #%d (ID: %s)", i, car.id)

                # Сериализуем ключ и значение в байты перед передачей в librdkafka
                key_bytes = self.key_serializer(car.id)
                val_bytes = self.value_serializer(car)

                produce_kwargs: dict[str, Any] = {
                    "topic": self.config.topic,
                    "key": key_bytes,
                    "value": val_bytes,
                    "on_delivery": self._delivery_report,
                }
                if self.config.partition is not None:
                    produce_kwargs["partition"] = self.config.partition

                # Вызов produce() асинхронно помещает сообщение в внутренний буфер librdkafka
                self.producer.produce(**produce_kwargs)

                # poll(0) вызывает обработку служебных событий и асинхронных колбэков delivery_report
                self.producer.poll(0)

            logger.info(
                "Сброс буфера (flush) и ожидание доставки всех %d сообщений...", MAX_MESSAGES
            )
            # flush() блокирует поток до тех пор, пока все сообщения из буфера не будут отправлены
            self.producer.flush()
            logger.info("Все %d сообщений успешно обработаны.", MAX_MESSAGES)

        except Exception as err:
            logger.exception("Непредвиденная ошибка в работе Producer: %s", err)


if __name__ == "__main__":
    app = KafkaProducerApp()
    app.run()
