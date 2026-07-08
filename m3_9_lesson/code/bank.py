import datetime
import time
from random import random,randint,choice

from confluent_kafka import Producer,Consumer

import logging



# Настройка форматирования логов с временем, именем логгера

logging.basicConfig(level=logging.INFO,
                    format='{asctime} - {name} {levelname} {message}',
                    style='{')

# Создаем логгер для текущего модуля
logger = logging.getLogger(__name__)

PRODUCER_CONFIG = {
    'bootstrap.servers': 'localhost:9092',
    'client.id':'bank_transactions'
}

CONSUMER_CONFIG = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'bank_group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': True
}

TOPIC = 'bank_transaction'

TRANSACTIONS_OPERATIONS = 15
CLIENT_FIO = ['Иванов','Петров','Сидоров','Романов']
TYPE_OPERATIONS = ['ОПЛАТА','ПОПОЛНЕНИЕ','СНЯТИЕ','ПРОВЕРКА БАЛАНСА']
BANKS = ['ВТБ','СБЕР','Альфа Банк','Россельхоз Банк']


def get_transaction_id():
    return f'TR_{int(time.time() * 1000)}_{randint(100,999)}'


def generate_trantion_data():
    """Генерируем данные транзакции"""
    client_fio = choice(CLIENT_FIO)
    bank = choice(BANKS)
    operation = choice(TYPE_OPERATIONS)
    amount = randint(1000,100_000)
    timestamp =  {datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}
    return f'Клиент {client_fio} выполнил операцию {operation} в банке {bank} на сумму {amount}, время операции: {timestamp}'

def delivery_callback(err,msg):
    if err:
        logger.error('Ошибка при отправке сообщения')
    else:
        logger.info(f'Сообщение отправлено в топик {msg.topic()},'
                    f'Партиция: {msg.partition()},'
                    f'Ключ сообщения: {msg.key()},'
                    f'Тело сообщения: {msg.value()}'
                    )

def send_tranctions():
    """Отправка данных в брокер"""
    producer = Producer(PRODUCER_CONFIG)
    logger.info(f'Отправка {TRANSACTIONS_OPERATIONS} транзакций...')
    logger.info(f'Дата отправки: {datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}')

    try:
        for i in range(TRANSACTIONS_OPERATIONS):
            #СОЗДАНИЕ ТРАНЗАКЦИИ
            transaction_id = get_transaction_id()
            transaction_data = generate_trantion_data()
            # Отправляем данные в Кафка
            producer.produce(topic=TOPIC,
                             key=transaction_id.encode('utf-8'),
                             value=transaction_data.encode('utf-8'),
                             callback=delivery_callback
                             )
            delay = 0.3 + random() * 0.7 #задержка от 300мс до 1000 мс
            time.sleep(delay)
            logger.debug(f'Создана транзакция {i + 1}: {transaction_id}')
        producer.flush() #ждем отправки всех сообщений
        logger.info(f'Все транзакции успешно выполнены!')
    except Exception as err:
        logger.error(f'Ошибка: {err}')


def get_info():
    consumer = Consumer(CONSUMER_CONFIG)
    consumer.subscribe([TOPIC])
    logger.info('Ожидание транзакций... (CTRL + C - выход)')

    try:
        count = 0
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                logger.error(f'Ошибка: {msg.error()}')
                continue
            count = count + 1
            key = msg.key().decode('utf-8')
            value = msg.value().decode('utf-8')
            logger.info(f'Транзакция №{count}')
            logger.info(f'ID {key}')
            logger.info(f'Данные {value}')
            logger.info('-' * 50)
    except KeyboardInterrupt as e:
        logger.info('Остановлено пользователем')
    except Exception as e:
        logger.info(f'Ошибка: {e}')
    finally:
        consumer.close()

def main():
    print("=" * 50)
    print("Банковская система")
    print("1) Выполнить транзакции")
    print("2) Получить информацию о транзакциях")
    print("3) Выход")

    match int(input("Выберите действие:")):
        case 1:
            send_tranctions()
        case 2:
            get_info()

if __name__ == '__main__':
    main()