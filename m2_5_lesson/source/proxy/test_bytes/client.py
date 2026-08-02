# from socket import *
from socket import AF_INET, SOCK_STREAM, socket

client = socket(AF_INET, SOCK_STREAM)

# Подключаемся к серверу

client.connect(('localhost', 8888))

data_from_server = client.recv(1024 * 100)

client.close()

print('Сервер ответил:', data_from_server.decode('UTF-8'))


# Сделать чат-бот между клиентом и сервером.
# Клиент может передавать запросы в виде любых математических действий, а сервер
# должен их принимать обрабатывать и возвращать клиенту верный ответ или сообщение
# об ошибке, если данные, полученные от клиента были некорректными.
