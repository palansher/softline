import json

from brand import Brand
from model import Model


class Deserializer:
    def deserializer(self, data: bytes) -> Model:
        try:
            if data is None:
                return None
            data_dict = json.loads(data.decode("utf-8"))
            return Model(
                # brand=data_dict["brand"]["name"],
                brand=Brand(data_dict["brand"]["name"],data_dict["brand"]["dop"]),
                model=data_dict["model"],
                price=data_dict["price"]
            )
        except json.decoder.JSONDecodeError as e:
            raise RuntimeError(f"Ошибка при парсинге данных: {e}")
        except Exception as e:
            raise RuntimeError(f"Ошибка при десериализации: {e}")

    def deserializer_key(self, data: bytes) -> int:
        try:
            if data is None:
                return None
            return int(data.decode("utf-8"))
        except Exception as e:
            raise RuntimeError(f"Ошибка при десериализации ключа: {e}")
