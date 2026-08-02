import time
from socket import AF_INET, SOCK_STREAM, socket

server = socket(AF_INET, SOCK_STREAM)
server.bind(('', 8888))
server.listen(5)

print("Сервер запущен и ожидает подключений...")

while True:
    # sock — сокет для общения, client_address — (IP, порт) клиента
    print('Жду подключений ..')
    sock, client_address = server.accept()
    print(f'Подключился клиент: {client_address}')
    
    # 1. Читаем данные, которые прислал клиент (максимум 1024 байта)
    print('Жду ответ клиента ..')
    raw_data = sock.recv(1024)
    # Декодируем байты в понятный текст
    client_message = raw_data.decode('UTF-8')
    print(f'Клиент прислал сообщение: "{client_message}"')
    
    # 2. Готовим и отправляем ответ
    answer = f'Привет! Я получил твое сообщение "{client_message}" в {time.ctime()}'
    sock.send(answer.encode('UTF-8'))
    
    # Закрываем соединение с этим клиентом
    sock.close()
