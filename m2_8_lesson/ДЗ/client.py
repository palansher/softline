from socket import *

client = socket(AF_INET, SOCK_STREAM)

# Подключаемся к серверу
client.connect(('localhost', 8888))
while True:
    operation = input("input math operation or type \"exit\" to exit\n")
    client.send(operation.encode('UTF-8'))
    data_from_server = client.recv(1024)
    print('Сервер ответил:', data_from_server.decode('UTF-8'))
    if data_from_server.decode('UTF-8') == "goodbye":
        break
client.close()

# Сделать чат-бот между клиентом и сервером.
# Клиент может передавать запросы в виде любых математических действий, а сервер
# должен их принимать обрабатывать и возвращать клиенту верный ответ или сообщение
# об ошибке, если данные, полученные от клиента были некорректными.
