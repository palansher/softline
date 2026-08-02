from office.Director import Director
from office.Economist import Economist
from office.Person import Person
from office.Programmer import Programmer

director = Director("Директор")
economist = Economist("Экономист")
programmer = Programmer("Программист")

man1 = Person("Иванов",director)
man2 = Person("Петров",economist)
man3 = Person("Сидоров",programmer)
man4 = Person("Романов",programmer)

for man in [man1,man2,man3,man4]:
    print(man.get_info())
