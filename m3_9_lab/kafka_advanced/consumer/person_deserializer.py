"""Модуль десериализации JSON в объект Person."""

import json

from person import Person


class PersonDeserializer:
    """Десериализатор сообщений Kafka из JSON-байтов в объект Person."""

    def __call__(self, data: bytes | None) -> Person | None:
        """Преобразует JSON-байты в объект Person."""
        # ОБРАБОТКА TOMBSTONE: В Kafka пустые сообщения (data=None) могут служить
        # маркерами удаления записи (Tombstone record). Возвращаем None без ошибки.
        if not data:
            return None
        try:
            data_str = data.decode("utf-8")
            data_dict = json.loads(data_str)
            return Person(
                id=data_dict["id"],
                firstname=data_dict["firstname"],
                lastname=data_dict["lastname"],
                salary=data_dict["salary"],
            )
        except (UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as err:
            raise RuntimeError(f"Ошибка при десериализации данных Person: {err}") from err
