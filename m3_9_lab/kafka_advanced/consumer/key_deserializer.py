"""Модуль десериализации ключей Kafka."""


class KeyDeserializer:
    """Десериализатор ключей сообщений Kafka из байтов UTF-8 в int."""

    def __call__(self, data: bytes | None) -> int | None:
        """Преобразует байтовый ключ в целое число."""
        # ПРОДАКШЕН-ПРАКТИКА: Безопасная обработка пустых ключей (Null keys).
        if not data:
            return None
        try:
            return int(data.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as err:
            raise RuntimeError(f"Ошибка при десериализации ключа Kafka: {err}") from err
