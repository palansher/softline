from Position import Position
from Person import Person
from firm.Company import Company

main_position = Position("Директор",500000)
position1 = Position("Программист",200000)
position2 = Position("DevOps",220000)
position3 = Position("QA инженер",160000)

positions = [position1,position2,position3]

my_company = Company("IT Start",positions,Person(1,"Романов",main_position))

# Добавляем сотрудников

for _ in range(3):
    my_company.add_man()

my_company.show_info()

my_company.change_salary(-50_000,3)
print("Информация о всех сотрудниках после изменения оклада:")
my_company.show_info()

# Увольняем сотрудника
my_company.remove_man(3)
print("Информация о всех сотрудниках после сокращения:")
my_company.show_info()