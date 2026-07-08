import json
from typing import Any
from kafka.serializer.abstract import Serializer


class CarSerializer(Serializer):
    """Сериализатор для объектов Person в JSON байты"""

    def __init__(self, **kwargs):
        pass

    def serialize(self, topic: str, data: Any) -> bytes:
        try:
            # Если объект имеет метод to_dict
            if hasattr(data, 'to_dict'):
                data_dict = data.to_dict()
            else:
                # Предполагаем, что это уже словарь
                data_dict = data
            # Преобразуем словарь в JSON и кодируем в байты UTF-8
            return json.dumps(data_dict).encode('UTF-8')
        except Exception as e:
            raise RuntimeError(f"Ошибка при сериализации: {str(e)}")

