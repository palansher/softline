import json

from Person import Person


class Deserializer:
    def deserialize(self, data:bytes) -> Person:
        try:
            if data is None:
                return None
            data_str = data.decode('utf-8')
            data_dict = json.loads(data_str)

            return Person(
                id=data_dict['id'],
                firstname=data_dict['firstname'],
                lastname=data_dict['lastname'],
                salary=data_dict['salary']
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
