from abc import ABC, abstractmethod


class Position(ABC):
    RATE = 50_000
    def __init__(self, title):
        self.title = title

    @abstractmethod
    def get_k(self):
        pass

    def calc_salary(self):
        """Расчет зп на основе коэффициента"""
        return Position.RATE * self.get_k()