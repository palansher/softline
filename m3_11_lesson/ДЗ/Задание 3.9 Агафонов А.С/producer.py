import logging
import random
from random import randint

from kafka import KafkaProducer

from brand import Brand
from key_serializer import KeySerializer
from model import Model
from model_serializer import ModelSerializer
from producer_config import ProducerConfig

# Настройка форматирования логов с временем, именем логгера

logging.basicConfig(level=logging.INFO,
                    format='{asctime} - {name} {levelname} {message}',
                    style='{')

# Создаем логгер для текущего модуля
logger = logging.getLogger(__name__)

BRAND_NAME = ['Audi', 'BMW', 'Mercedes']
MODEL_NAME = ['Sedan', 'Coupe', 'Surf']

TOTAL_MESSAGES = 10


def create_model(brand: Brand, name: str, price: float) -> Model:
    return Model(
        brand=brand,
        model=name,
        price=price)


class Producer:
    def __init__(self):
        self.value_serializer = ModelSerializer()
        self.key_serializer = KeySerializer()
        self.producer = None

    # 1. Коллбэк для успешной отправки
    def _on_success(self, record_metadata):
        logger.info(
            f"Сообщение успешно отправлено в топик '{record_metadata.topic}' "
            f"[партиция: {record_metadata.partition}, офсет: {record_metadata.offset}]"
        )

    # 2. Коллбэк для обработки ошибок доставки
    def _on_error(self, exception):
        # Здесь можно настроить отправку в базу данных, повторную очередь (DLQ) или алерты
        logger.error(f"Ошибка при доставке сообщения в Kafka: {exception}", exc_info=True)

    def start_producer(self):
        try:
            self.producer = KafkaProducer(
                **ProducerConfig.get_producer_config(),
                key_serializer=self.key_serializer,
                value_serializer=self.value_serializer
            )
            logger.info("Продюсер запущен!")
        except Exception as e:
            logger.error(f"Error: {e}")
            raise

    def send_message(self):
        if not self.producer:
            raise RuntimeError('Продюсер не запущен! Вызовите метод start_producer')
        try:
            for i in range(TOTAL_MESSAGES):
                # Заполняем случайными значениями наши классы
                brand = Brand(random.choice(BRAND_NAME), randint(2010, 2026))
                model = create_model(brand, random.choice(MODEL_NAME), random.randint(1000, 1500))
                async_producer = self.producer.send(
                    topic=ProducerConfig.TOPIC,
                    partition=ProducerConfig.PARTITION,
                    key=i + 1,
                    value=model
                )
                async_producer.add_callback(self._on_success)
                async_producer.add_errback(self._on_error)
            self.producer.flush()
            logger.info(f"Produced send {TOTAL_MESSAGES} messages")
        except Exception as e:
            logger.error(f"Ошибка при подготовки сообщения: {e}")
        finally:
            if self.producer:
                self.producer.close()
                logger.info(f"Closed producer")


if __name__ == "__main__":
    app = Producer()
    app.start_producer()
    app.send_message()
