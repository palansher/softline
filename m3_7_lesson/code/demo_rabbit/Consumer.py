import pika
from pika import callback

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.queue_declare(queue='lesson7')


# Подписываем получателя к этой очереди

def callback(ch,method,props,body):
    print(f'Сообщение {body.decode()} получено!')

channel.basic_consume(queue='lesson7',on_message_callback=callback,auto_ack=True)

try:
    channel.start_consuming() #включаем бесконечный цикл ожидания сообщений из брокер
except KeyboardInterrupt:
    # Разрываем соединение консьюмера с брокера по нажатию клавиши CTRL + C
    connection.close()