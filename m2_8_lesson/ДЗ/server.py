# IP - это идентификатор вычислительного устройства. Порт это число, уникальное для данного устройства.
# В рамках ОС за определенным портом закрепляется только одно приложение
import time
from socket import *

# СЛУЖБА    ПОРТ
# FTP      20, 21
# SMTP       25
# HTTP       80
# TELNET     23
# SSH        22

# Сетевые сокеты работают по протоколу TCP/IP
# AF_INET - указываем, что сокет сетевой
# SOCK_STREAM - указываем, что сокет потоковый
server = socket(AF_INET, SOCK_STREAM)
server.bind(('', 8888))
server.listen(5) #допускаем до 5 запросов одновременно
sock, data_from_client = server.accept()
while True:
    operation = sock.recv(1024).decode('UTF-8')
    if operation == 'exit':
        answer = "goodbye"
        sock.send(answer.encode('UTF-8'))
        break
    else:
        try:
            # Готовим ответ клиенту
            answer = str(eval(operation))
        except NameError:
            answer = "incorrect input"
    print(f'Получен запрос от клиента с данными {data_from_client}')
    # Шифруем строку для отправки клиенту
    sock.send(answer.encode('UTF-8'))
sock.close()