class Person:
    def __init__(self,name,salary):
        self.salary = salary
        self.name = name

    def get_info(self):
        return f"Сотрудник {self.name} получает оклад {self.salary}"

class Manager(Person):
    def __init__(self,name,salary,role):
        super().__init__(name,salary)
        self.role = role

    def get_info(self):
        return f"{super().get_info()} с ролью {self.role}"

    def add_bonus(self):
        print("Премия 10000")

man1 = Person("Петров", 1000)
# print(man1.get_info())
man2 = Manager("Иванов",1200, "директор")
man3 = Manager("Сидоров",1200, "Начальник отдела")
# print(man2.get_info())

# print(isinstance(man1,Manager))

men = [man1,man2,man3]
for man in men:
    print(man.get_info())
    if isinstance(man, Manager):
        man.add_bonus()
