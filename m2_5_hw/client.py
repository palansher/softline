# пользователь взаимодействует исключительно с классом ClientProxy

from network import RealClient
from proxy import ClientProxy, MathClientInterface


def main() -> None:
    # 1. Создаем реальный клиент для работы с сетью
    real_client = RealClient()

    # 2. Оборачиваем его в Proxy для валидации
    proxy_client: MathClientInterface = ClientProxy(real_client)

    try:
        real_client.connect()
    except ConnectionRefusedError:
        print("Не удалось подключиться к серверу. Убедитесь, что server.py запущен.")
        return

    print("\n--- Чат-бот: Математический клиент-сервер ---")
    print("Вводите математические выражения (например: 2 + 2 * 2).")
    print("Для выхода введите 'exit' или 'quit'.\n")

    try:
        while True:
            user_input: str = input("Вы: ")

            if user_input.lower() in ["exit", "quit"]:
                print("Завершение работы...")
                break

            # Отправляем запрос через Proxy
            response: str = proxy_client.send_expression(user_input)
            print(f"Ответ: {response}\n")

    finally:
        real_client.close()


if __name__ == "__main__":
    main()
