from Position import Position


class Person:
    def __init__(self,id, fio,position):
        self.position = position
        self.fio = fio
        self.id = id
        self.salary = position.salary

    def add_profit(self,size):
        self.salary += size

    def get_info(self):
        return f"Сотрудник {self.fio} в должности {self.position.title} зарабатывает {self.salary}"

position1 = Position("Программист",200000)
position2 = Position("DevOps",220000)
position3 = Position("QA инженер",160000)

man1 = Person(1,"Иванов",position1)
man2 = Person(2,"Петров",position2)
man3 = Person(3,"Сидоров",position3)

man2.add_profit(100000)



men = [man1,man2,man3]
for man in men:
    print(man.get_info())