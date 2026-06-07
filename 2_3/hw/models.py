import random

class CarNumber:
    """
    Описывает структуру российского автомобильного номера
    """
    
    # Список разрешенных кириллических букв для номеров РФ
    ALLOWED_LETTERS = "АВЕКМНОРСТУХ"

    def __init__(self, number_str: str):
        """
        Инициализирует объект номера.
        
        :param number_str: Полная строка номера.
        """
        self.full_number: str = number_str.upper()

    @classmethod
    def generate_random(cls, region: str) -> 'CarNumber':
        """
        Генерирует случайный номер на основе региона.
        
        :param region: Код региона.
        :return: Экземпляр CarNumber.
        """
        letters = [random.choice(cls.ALLOWED_LETTERS) for _ in range(3)]
        digits = "".join([str(random.randint(0, 9)) for _ in range(3)])
        formatted_str = f"{letters[0]}{digits}{letters[1]}{letters[2]}{region}"
        return cls(formatted_str)

    @staticmethod
    def is_valid(number_str: str) -> bool:
        """
        Проверяет номер на валидность (длина 8-9 символов).
        Алгоритм генерации номера и так создает валидный номер с нужной длиной, поэтому - этот метод - только красоты для демонстрации
        
        :param number_str: Строка номера.
        """
        return 8 <= len(number_str) <= 9
    