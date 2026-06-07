from socket import AF_INET, SOCK_STREAM, socket

client = socket(AF_INET, SOCK_STREAM)
client.connect(('localhost', 8888))

# 1. Формируем сообщение и отправляем его на сервер
# Текст обязательно нужно закодировать в байты (.encode())
message = "Привет, сервер! Как дела?"
client.send(message.encode('UTF-8'))
print(f'Вы отправили серверу: "{message}"')

# 2. Ждем ответ от сервера
data_from_server = client.recv(1024 * 100)
print('Сервер ответил:', data_from_server.decode('UTF-8'))

client.close()
