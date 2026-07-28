import pika

# BlockingConnection - это синхронное соединение
# ConnectionParameters - это параметры подключения

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

# Все операции с RabbitMQ через канал связи
channel = connection.channel()

# Объявляем очередь
channel.queue_declare(queue='lesson7')

channel.basic_publish(exchange='',routing_key='lesson7',body='Привет!')

print('Сообщение успешно отправлено в Брокер')

connection.close()