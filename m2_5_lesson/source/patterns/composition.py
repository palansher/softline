from abc import ABC, abstractmethod


class SimpleGraphicItem(ABC):
    @abstractmethod
    def draw(self):
        pass

class Line(SimpleGraphicItem):
    def draw(self):
        print("Рисуем прямую линию")

class Rectangle(SimpleGraphicItem):
    def draw(self):
        print("Рисуем прямоугольник")

class GroupItems(SimpleGraphicItem):
    def __init__(self):
        self.items = []

    def add_item(self,item):
        self.items.append(item)

    def draw(self):
        for item in self.items:
            item.draw()


line1 = Line()
line2 = Line()
rect = Rectangle()
group = GroupItems()
group.add_item(line1)
group.add_item(line2)
group.add_item(rect)
group.draw()
