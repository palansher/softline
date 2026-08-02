from AutoWerke import AutoWerke, AddOptions
from Kuzov import Kuzov
from Shassi import Shassi
from Glass import Glass
from Transmission import Transmission
from Engine import Engine
from Condition import Condition
from Kovriki import Kovriki
from Signal import Signal
 
class CreateAuto(AutoWerke, AddOptions):
    """Автомобиль"""

    def __init__(self,title_auto):
        """Конструктор класса. Инициализируем свойство название автомобиля"""
        self.title_auto = title_auto

    def create_kuzov(self,type):
        """Создание кузова"""
        self.__setattr__('kuzov',Kuzov(type))
        return self

    def create_shassi(self,type):
        """Тип шасси"""
        self.__setattr__('shassi',Shassi(type))
        return self

    def create_transmission(self,type):
        """Создание трансмисси"""
        self.__setattr__('transmission',Transmission(type))
        return self

    def create_glass(self,type):
        """Создание остекления"""
        self.__setattr__('glass',Glass(type))
        return self

    def create_engine(self,type):
        """Создание двигателя"""
        self.__setattr__('engine',Engine(type))
        return self

    def mount_condition(self,type):
        """Установка кондиционера"""
        self.__setattr__('condition',Condition(type))
        return self

    def mount_kovriki(self,type):
        """Установка ковриков"""
        self.__setattr__('kovriki',Kovriki(type))
        return self

    def mount_signal(self,type):
        """Установка ковриков"""
        self.__setattr__('signal',Signal(type))
        return self

    def show_info_Auto(self):
        """Вывод иноформации о созданном автомобиле"""
        print(f'{"*"*20}')
        print(f'Автомобиль - {self.title_auto}')

        print(f'ОСНОВНЫЕ ОПЦИИ {"="*105}')
        for item in self.get_base_options():
            print(f'|{item:<25}', end='')
        print(f'\n{"="*115}')

        if hasattr(self, 'kuzov'):
            print(f'|{str(self.kuzov):<25}', end='')
        if hasattr(self, 'shassi'):
            print(f'|{str(self.shassi):<25}', end='')
        if hasattr(self, 'transmission'):
            print(f'|{str(self.transmission):<25}', end='')
        if hasattr(self, 'glass'):
            print(f'|{str(self.glass):<25}', end='')
        if hasattr(self, 'engine'):
            print(f'|{str(self.engine):<25}', end='')

        print(f'\n\nДОПОЛНИТЕЛЬНЫЕ ОПЦИИ {"="*99}')
        for item in self.get_add_options():
            print(f'|{item:<25}', end='')
        print(f'\n{"="*119}')

        if hasattr(self, 'condition'):
            print(f'|{str(self.condition):<25}', end='')
        else:
            print(f'|{"Без кондиционера":<25}', end='')
        if hasattr(self, 'kovriki'):
            print(f'|{str(self.kovriki):<25}', end='')
        else:
            print(f'|{"Без ковриков":<25}', end='')
        if hasattr(self, 'signal'):
            print(f'|{str(self.signal):<25}', end='')
        else:
            print(f'|{"Без сигнализации":<25}')
