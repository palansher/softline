"""Модель сериализации ключей Kafka."""

from typing import Any


# ПРОДАКШЕН-ПРАКТИКА: Паттерн Callable Class (реализация через __call__).
# Позволяет передавать класс в value_serializer / key_serializer как функцию,
# при этом сохраняя возможности ООП (инкапсуляция логики, валидация).
class KeySerializer:
    """Сериализатор ключей сообщений Kafka в байты UTF-8."""

    def __call__(self, key: Any) -> bytes:
        """Преобразует ключ в байтовый формат."""
        if key is None:
            return b""
        return str(key).encode("utf-8")
