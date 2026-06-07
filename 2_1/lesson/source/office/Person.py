class Person:
    def __init__(self,id, fio, salary):
        self.salary = salary
        self.fio = fio
        self.id = id

    def get_info(self):
        return f"Сотрудник {self.fio} зарабатывает {self.salary}"

man1 = Person(1,"Иванов",120000)
man2 = Person(2,"Петров",150000)
man3 = Person(3,"Сидоров",130000)

men = [man1,man2,man3]
for man in men:
    print(man.get_info())

