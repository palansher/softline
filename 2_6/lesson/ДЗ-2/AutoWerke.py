from abc import ABC, abstractmethod

class AutoWerke(ABC):
    """Автозавод"""

    __base_list = ['Кузов','Шасси','Трансмиссия','Остекление','Двигатель']

    @classmethod
    def get_base_options(cls):
        return cls.__base_list

    @abstractmethod
    def create_kuzov(self):
        """Кузов автомобиля"""
        pass

    @abstractmethod
    def create_shassi(self):
        """Кузов шасси"""
        pass

    @abstractmethod
    def create_transmission(self):
        """Трансмиссия автомобиля"""
        pass

    @abstractmethod
    def create_glass(self):
        """Остекление автомобиля"""
        pass

    @abstractmethod
    def create_engine(self):
        """Двигатель автомобиля"""
        pass


class AddOptions(ABC):
    """Дополнителельные опции"""

    __add_list = ['Кондиционер','Коврики','Сигнализация']

    @classmethod
    def get_add_options(cls):
        return cls.__add_list

    @abstractmethod
    def mount_condition(self):
        """Установка кондиционера"""
        pass

    @abstractmethod
    def mount_kovriki(self):
        """Установка ковриков"""
        pass

    @abstractmethod
    def mount_signal(self):
        """Установка cигнализации"""
        pass
