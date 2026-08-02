"""
Сетевая логика Socket
Здесь классы, отвечающие за сокет-соединение:
    Server (принимает и вычисляет через eval) и RealClient (отправляет байты в сеть).
"""

import socket
from proxy import MathClientInterface


class Server:
    """Класс TCP-сервера, принимающий выражения и вычисляющий их через eval."""

    def __init__(self, host: str = "127.0.0.1", port: int = 65432) -> None:
        self.host: str = host
        self.port: int = port
        self.buffer_size: int = 1024

    def start(self) -> None:
        """Запуск сервера в бесконечном цикле прослушивания."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Позволяет повторно использовать адрес сокета сразу после перезапуска
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f"[Сервер] Запущен на {self.host}:{self.port}. Ожидание клиентов...")

            while True:
                conn, addr = server_socket.accept()
                with conn:
                    while True:
                        print(f"[Сервер] Подключился клиент: {addr}")
                        data = conn.recv(self.buffer_size)
                        if not data:
                            break

                        expression: str = data.decode("utf-8")
                        print(f"[Сервер] Получено выражение: {expression}")

                        # Обработка выражения через eval
                        result: str = self._calculate(expression)
                        conn.sendall(result.encode("utf-8"))
                    print(f"[Сервер] Клиент {addr} отключился.")

    def _calculate(self, expression: str) -> str:
        """Вычисляет мат. выражение и возвращает значение строкой.
        Безопасность гарантируется проверкой Proxy.
        """
        try:
            # Ограничиваем eval, убирая доступ к глобальным/локальным переменным (__builtins__)
            res = eval(expression, {"__builtins__": None}, {})
            return str(res)
        except ZeroDivisionError:
            return "Ошибка [Сервер]: Деление на ноль!"
        except Exception as e:
            return f"Ошибка [Сервер]: Не удалось вычислить ({e})"


class RealClient(MathClientInterface):
    """Реальный клиент, который устанавливает соединение и общается с сервером."""

    def __init__(self, host: str = "127.0.0.1", port: int = 65432) -> None:
        self.host: str = host
        self.port: int = port
        self.buffer_size: int = 1024
        self.sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self) -> None:
        """Устанавливает соединение с сервером."""
        self.sock.connect((self.host, self.port))
        print("[Клиент] Успешно подключен к серверу.")

    def send_expression(self, expression: str) -> str:
        """Отправляет строку на сервер и возвращает текстовый ответ."""
        try:
            self.sock.sendall(expression.encode("utf-8"))
            response: bytes = self.sock.recv(self.buffer_size)
            return response.decode("utf-8")
        except Exception as e:
            return f"Ошибка сети: {e}"

    def close(self) -> None:
        """Закрывает сокет."""
        self.sock.close()
