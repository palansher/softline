import json

from Car import *

class Deserializer:
    def deserialize(self, data:bytes) -> CarModel:
        try:
            if data is None:
                return None
            data_str = data.decode('utf-8')
            data_dict = json.loads(data_str)

            return CarModel(
                id=data_dict['id'],
                mark=data_dict['mark'],
                model=data_dict['model']
            )
        except json.JSONDecodeError as e:
            raise RuntimeError(f'Ошибка парсинга {e}')
        except Exception as e:
            raise RuntimeError(f'Ошибка при десериализации {e}')

    def deserialize_key(self,data:bytes) -> int:
        try:
            if data is None:
                return None
            return int(data.decode('utf-8'))
        except Exception as e:
            raise RuntimeError(f'Ошибка при десериализации ключа {e}')
