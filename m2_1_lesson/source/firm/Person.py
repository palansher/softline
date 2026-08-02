from Position import Position


class Person:
    def __init__(self,id, fio,position):
        self.position = position
        self.fio = fio
        self.id = id
        self.salary = position.salary

    def __str__(self):
        return f"Сотрудник {self.fio} в должности {self.position.title} зарабатывает {self.salary}"

    # def get_info(self):
    #     return f"Сотрудник {self.fio} в должности {self.position.title} зарабатывает {self.salary}"

# man = Person(1,'Иванов',Position("QA","111"))
# print(man)