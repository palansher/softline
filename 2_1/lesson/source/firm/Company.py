import random

from firm.Person import Person


class Company():
    def __init__(self,title,positions,director):
        self.positions = positions
        self.men = [director]
        self.title = title

    def show_info(self):
        print(f"В компании {self.title} работают {len(self.men)} сотрудников включая директора:")
        for i in range(1,len(self.men)):
            print(self.men[i])
    def add_man(self):
        fio = input("Введите имя сотрудника\n")
        new_man = Person(len(self.men) + 1,fio,random.choice(self.positions))
        self.men.append(new_man)
        print(f"Сотрудник {fio} устроен на работу в должнотси: {new_man.position.title}")

    def change_salary(self,size,person_id):
        person = list(filter(lambda p: p.id == person_id,self.men))[0]
        """Премия/взыскание для сотрудника"""
        if size > 0:
            print(f"Сотрудник {person.fio} получает премию {size}")
        elif size < 0:
            print(f"Сотрудник {person.fio} получает взыскание {size}")
        person.salary += size

    def remove_man(self,person_id):
        count_men = len(self.men)
        person = list(filter(lambda p: p.id == person_id, self.men))[0]
        self.men.remove(person)
        print("Сотрудник уволен" if len(self.men) == count_men - 1 else "Сотрудник не найден")


# Создайте метод для увольнения сотрудника. Метод принимает id сотрудника, которого нужно уволить
# Вывести в main список сотрудников после увольнения