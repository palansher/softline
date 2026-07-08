from kafka import KafkaProducer
from kafka.errors import KafkaError

import logging
from datetime import datetime

from Person import Person
from config import ProducerConfig
from person_serializer import PersonSerializer
from key_serializer import KeySerializer  # Новый импорт

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

MAX_MESSAGES = 10


class KafkaProducerApp:
    def __init__(self):
        self.value_serializer = PersonSerializer()
        self.key_serializer = KeySerializer()
        self.producer = None

    def create_person(self, i: int) -> Person:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return Person(
            id=i,
            firstname=f"firstname-{current_time}",
            lastname=f"lastname {i}",
            salary=(i + 1) * 10
        )

    def run(self):
        try:
            self.producer = KafkaProducer(
                **ProducerConfig.get_producer_config(),
                key_serializer=self.key_serializer,
                value_serializer=self.value_serializer
            )

            for i in range(MAX_MESSAGES):
                person = self.create_person(i)

                self.producer.send(
                    topic=ProducerConfig.TOPIC,
                    partition=ProducerConfig.PARTITION,
                    timestamp_ms=int(datetime.now().timestamp() * 1000),
                    key=person.id,
                    value=person
                )
                logger.info(f'Sending message {i}')

            self.producer.flush()
            logger.info(f'Successfully sent {MAX_MESSAGES} messages')

        except Exception as e:
            logger.error(f"Error: {e}")

        finally:
            if self.producer:
                self.producer.close()
                logger.info('Кафка продюсер закрыт')


if __name__ == '__main__':
    app = KafkaProducerApp()
    app.run()