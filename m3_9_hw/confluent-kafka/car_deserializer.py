"""Модуль десериализации JSON в объект Car."""

import json

from car import Car


class CarDeserializer:
    """Десериализатор сообщений Kafka из JSON-байтов в объект Car."""

    def __call__(self, data: bytes | None) -> Car | None:
        """Преобразует JSON-байты в объект Car."""
        # ОБРАБОТКА TOMBSTONE: В Kafka пустые сообщения (data=None) могут служить
        # маркерами удаления записи (Tombstone record). Возвращаем None без ошибки.
        if not data:
            return None
        try:
            data_str = data.decode("utf-8")
            data_dict = json.loads(data_str)
            return Car(
                id=data_dict["id"],
                model=data_dict["model"],
                year=data_dict["year"],
                category=data_dict["category"],
                vin=data_dict["vin"],
                color=data_dict["color"],
                brand=data_dict["brand"],
            )
        except (UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as err:
            raise RuntimeError(f"Ошибка при десериализации данных Car: {err}") from err
