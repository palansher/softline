class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __eq__(self, man):
        return self.name == man.name and self.age == man.age


man1 = Person("Иванов", 18)
man2 = Person("Иванов", 18)

print(man1 == man2)