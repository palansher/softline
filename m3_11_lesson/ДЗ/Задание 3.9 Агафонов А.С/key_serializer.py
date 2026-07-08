from typing import Any

from kafka import KafkaProducer


class KeySerializer:
    def __init__(self, **kwargs):
        pass

    # Этот метод будет вызывать kafka-python
    def __call__(self, key: Any) -> bytes:
        return self.serialize(topic="", key=key)

    def serialize(self, topic: str, key) -> bytes:
        if key is None:
            return None
        return str(key).encode("utf-8")

    def close(self):
        pass

