"""Модель сериализации объектов в JSON-байты."""

import json
from typing import Any


class ObjSerializer:
    """Сериализатор объектов или словарей в формат JSON (bytes)."""

    def __call__(self, data: Any) -> bytes:
        """Сериализует входной объект в JSON-строку, закодированную в UTF-8."""
        try:
            # Поддержка как объектов Car (через to_dict), так и обычных словарей
            data_dict = data.to_dict() if hasattr(data, "to_dict") else data
            return json.dumps(data_dict, ensure_ascii=False).encode("utf-8")
        except (TypeError, ValueError) as err:
            # Перехватываем низкоуровневые ошибки сериализации и оборачиваем в понятный RuntimeError
            raise RuntimeError(f"Ошибка при сериализации данных {data}: {err}") from err
