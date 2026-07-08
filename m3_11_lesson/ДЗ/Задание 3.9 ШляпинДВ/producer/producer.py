from kafka import KafkaProducer
from kafka.errors import KafkaError
from random import choice

import logging
from datetime import datetime

from Car import *
from config import ProducerConfig
from car_serializer import CarSerializer
from key_serializer import KeySerializer  # Новый импорт

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

MAX_MESSAGES = 10


class KafkaProducerApp:
    def __init__(self):
        self.value_serializer = CarSerializer()
        self.key_serializer = KeySerializer()
        self.producer = None

    def create_car(self,  i: int) -> CarModel:
        marks = ["BMV", "Audi", "Tesla", "Lexus", "Infiniti"]
        mark = choice(marks)
        models = ['Модель_1', "Модель_2", "Модель_3", "Модель_4", "Модель_5","Модель_6","Модель_7","Модель_8","Модель_9","Модель_10"]
        model = choice(models)
       
        return CarModel(
            id=i,
            mark=mark,
            model=model
        )

    def run(self):
        try:
            self.producer = KafkaProducer(
                **ProducerConfig.get_producer_config(),
                key_serializer=self.key_serializer,
                value_serializer=self.value_serializer
            )

            for i in range(MAX_MESSAGES):
                car = self.create_car(i)

                self.producer.send(
                    topic=ProducerConfig.TOPIC,
                    partition=ProducerConfig.PARTITION,
                    timestamp_ms=int(datetime.now().timestamp() * 1000),
                    key=car.id,
                    value=car
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