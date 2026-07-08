# Настройка форматирования логов с временем, именем логгера
import logging

from kafka import KafkaConsumer
from kafka.errors import KafkaError

from consumer_config import ConsumerConfig
from model import Model
from model_deserializer import Deserializer

logging.basicConfig(level=logging.INFO,
                    format='{asctime} - {name} {levelname} {message}',
                    style='{')

# Создаем логгер для текущего модуля
logger = logging.getLogger(__name__)

TOTAL_MESSAGES = 10

class Consumer(object):
    def __init__(self):
        self.deserializer = Deserializer()
        self.consumer = None

    def start(self):
        try:
            self.consumer = KafkaConsumer(
                ConsumerConfig.TOPIC,
                **ConsumerConfig.get_consumer_config(),
                key_deserializer = lambda key: self.deserializer.deserializer_key(key),
                value_deserializer = lambda val: self.deserializer.deserializer(val)
            )
            logger.info("Consumer started")
            msg_received = 0

            for message in self.consumer:
                model: Model = message.value
                key = message.key
                logger.info(f'Получено сообщение: {msg_received + 1}: '
                            f'key: {key}, '
                            f'Модель: {model.brand.name} ({model.model}) {model.brand.dop} года выпуска стоит {model.price} у.е.'
                            # f'Модель: производитель: {model.brand} ({model.model}) {model.dop} года выпуска стоит {model.price} у.е.'
                            f'offset {message.offset})')
                msg_received += 1
                if msg_received >= TOTAL_MESSAGES:
                    break
                if msg_received == 0:
                    logger.warning('Тайм-аут при получении сообщений')
                else:
                    logger.info(f'Всего получено сообщений: {msg_received}')
        except KafkaError as e:
            logger.error(f'Kafka error: {e}')
        except Exception as e:
            logger.error(f'Ошибка: {e}')
        finally:
            if self.consumer is not None:
                self.consumer.close()
                logger.info(f'Consumer closed')

if __name__ == '__main__':
    consumer = Consumer()
    consumer.start()