class Man:
    def __init__(self, name, age):
        self.name = name
        self.age = age

man1 = Man('Иван', 18)
# man2 = man1 передача значения по ссылке, т.е. меняя man2 - будет менятья и man1

import copy
man2 = copy.copy(man1)
man2.age = 20

print(man1.age)
