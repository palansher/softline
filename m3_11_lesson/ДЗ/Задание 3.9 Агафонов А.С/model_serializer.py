import json
from typing import Any
from kafka.serializer.abstract import Serializer


class ModelSerializer(Serializer):

    def __init__(self, **kwargs):
        pass

    # Этот метод будет вызывать kafka-python
    def __call__(self, data: Any) -> bytes:
        return self.serialize(topic="", data=data)

    def serialize(self, topic: str, data: Any) -> bytes:
        try:
            if hasattr(data, "to_dict"):
                data_dict = data.to_dict()
            else:
                data_dict = data
            return json.dumps(data_dict).encode("utf-8")
        except Exception as e:
            raise RuntimeError(f"Ошибка при сериализации: {e}")
