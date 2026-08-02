# Статические методы - это методы, которые являются обычными функциями, заданными в классе.
# Статические методы - универсальные команды, которые не изменяют свойства объекта, т.к. использовать
# self в таких методах строго запрещено. Статические методы можно вызывать по имени класса, но можно и по имени
# объекта

class Person:
    def __init__(self,name,age):
        self.name = name
        self.age = age

    # def compare_age(self,person):
    # """Вариант верный и тоже оптимальный"""
    #     if self.age > person.age:
    #         print(f'{self.name} старше {person.name}')
    #     elif self.age < person.age:
    #         print(f'{self.name} младше {person.name}')
    #     else:
    #         print('Ровестники')

    @staticmethod
    def compare_age(person1,person2):
        if person1.age > person2.age:
            print(f'{person1.name} старше {person2.name}')
        elif person1.age < person2.age:
            print(f'{person1.name} младше {person2.name}')
        else:
            print('Ровестники')

man1 = Person('Иван',20)
man2 = Person('Олег',30)
Person.compare_age(man1,man2)