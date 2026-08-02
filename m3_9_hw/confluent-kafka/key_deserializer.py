"""Модуль десериализации ключей Kafka."""


class KeyDeserializer:
    """Десериализатор ключей сообщений Kafka из байтов UTF-8"""

    def __call__(self, data: bytes | None) -> str | None:
        """Преобразует байтовый ключ в строку."""
        # ПРОДАКШЕН-ПРАКТИКА: Безопасная обработка пустых ключей (Null keys).
        if not data:
            return None
        try:
            # return int(data.decode("utf-8"))
            return data.decode("utf-8")
        except (UnicodeDecodeError, ValueError) as err:
            raise RuntimeError(f"Ошибка при десериализации ключа Kafka: {err}") from err
