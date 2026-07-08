from kafka.serializer.abstract import Serializer


class KeySerializer(Serializer):
    """Сериализатор для ключей"""

    def __init__(self, **kwargs):
        pass

    def serialize(self, topic: str, key) -> bytes:
        if key is None:
            return None
        return str(key).encode('UTF-8')

    def close(self):
        pass