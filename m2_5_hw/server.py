"""
Точка входа Сервера
для инициализации и запуска сервера
"""

from network import Server

def main() -> None:
    server = Server()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n[Сервер] Остановлен пользователем.")

if __name__ == "__main__":
    main()
