import logging

from kafka import KafkaConsumer

from kafka_advanced.consumer import Person
from kafka_advanced.consumer.config import KafkaConsumerConfig
from kafka_advanced.consumer.person_deserializer import Deserializer
from kafka_advanced.producer.person_serializer import PersonSerializer

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

MAX_MESSAGES = 10
POLL_TIMEOUT_TO_CONSUMER = 1000 #ТАЙМАУТ для опроса в мс

class KafkaConsumerApp:
    def __init__(self):
        self.deserializer = Deserializer()
        self.consumer = None

    def run(self):
        try:
            self.consumer = KafkaConsumer(
                KafkaConsumerConfig.TOPIC,
                **KafkaConsumerConfig.get_consumer_config(),
                key_deserializer = lambda k: self.deserializer.deserialize_key(k),
                value_deserializer = lambda v: self.deserializer.deserialize(v),
                consumer_timeout_ms = 10000
            )
            logger.info("consumer started")
            messages_received = 0

            for message in self.consumer:
                person: Person = message.value
                key = message.key
                logger.info(f'Получено сообщение: {messages_received + 1}: '
                            f'key: {key},'
                            f' id: {person.id}',
                            f' Имя: {person.firstname}',
                            f' Фамилия: {person.lastname}',
                            f'Зарплата: {person.salary}',
                            f'offset: {message.offset}')
                messages_received += 1

                if messages_received >= MAX_MESSAGES:
                    break
                if messages_received == 0:
                    logger.warning('Сообщения не получены в течение таймаута')
                else:
                    logger.info(f"Всего получено сообщений: {messages_received}")

        except Exception as e:
            logger.error(f'Ошибка {e}')

        finally:
            if self.consumer is not None:
                self.consumer.close()
                logger.info("consumer closed")

if __name__ == '__main__':
    app = KafkaConsumerApp()
    app.run()