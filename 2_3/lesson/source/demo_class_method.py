import datetime


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return "Name: {}, Age: {}".format(self.name, self.age)

    @classmethod
    def create_person(cls, name, year_of_birth):
        age = datetime.datetime.now().year - year_of_birth
        return cls(name, age)

man = Person.create_person("Иванов", 2000)
print(man)