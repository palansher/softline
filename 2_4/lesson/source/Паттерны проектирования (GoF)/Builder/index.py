from abc import ABC, abstractmethod


class Builder(ABC):
    @abstractmethod
    def build_base(self):
        """Строим фундамент дома"""
        pass

    @abstractmethod
    def build_box(self):
        """Коробка дома"""
        pass
    @abstractmethod
    def build_roof(self):
        """Крыша дома"""
    @abstractmethod
    def build_field_golf(self):
        """Поле для гольфа"""


class Base:
    def __init__(self, type):
        self.type = type
    def __str__(self):
        return f'{self.type}'

class Box:
    def __init__(self, type):
        self.type = type
    def __str__(self):
        return f'{self.type}'


class Roof:
    def __init__(self, type):
        self.type = type

    def __str__(self):
        return f'{self.type}'


class Golf:
    def __init__(self, area):
        self.area = area

    def __str__(self):
        return f'Заложено поле под гольф площадью {self.area} кв.км'

class House(Builder):
    def build_base(self,type):
        self.__setattr__('base',Base(type))
        return self
    def build_box(self,type):
        self.__setattr__('box',Box(type))
        return self
    def build_roof(self,type):
        self.__setattr__('roof',Roof(type))
        return self
    def build_field_golf(self,type):
        self.__setattr__('field_golf',Golf(type))
        return self
    def show_info_house(self):
        if hasattr(self, 'base'):
            print('Дом имеет фундамент типа ',self.base)

        if hasattr(self, 'box'):
            print('Дом построен из материала', self.box)

        if hasattr(self, 'roof'):
            print('Крыша дома построена из материала', self.roof)

        if hasattr(self, 'field_golf'):
            print(self.field_golf)

house = House().build_base('Ленточный').build_box('Кирпич').build_roof('Металллочерепица')
house.show_info_house()