class Person:
    count = 0
    def __init__(self,fio):
        Person.count += 1
        self.id = Person.count
        self.fio = fio

    def __str__(self):
        return f"ID:{self.id}, ФИО:{self.fio}\n"

man1 = Person("Вася")
man2 = Person("Петя")

print(man1, man2)

