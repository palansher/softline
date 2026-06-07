"""
main - Created on 11.10.2025 11:18
Демонстрация системы
"""
import random

from Univer.Faculty import Faculty
from Univer.Student import Student
from Univer.University import University


def get_num(ques: str) -> int:
    # Функция для получения числа с клавиатуры
    num = input(ques)
    if num.isdigit():
        return int(num)
    else:
        print("Вы ввели некорректное значение")
        return get_num(ques)

    # создаем новый университет


my_univer = University("МАГУ")

# создаем факультеты
my_univer.add_faculty(Faculty("Наук"))
my_univer.add_faculty(Faculty("Искусств"))
my_univer.add_faculty(Faculty("Финансов"))

# зачисляем новых студентов
print("*" * 50)
print(f"Зачисляем в Университет {my_univer.university_name} 5 студентов")

for _ in range(5):
    random.choice(my_univer.faculties).add_student()

my_univer.get_all_students()

# переводим студента на другой факультет
print("*" * 50)
is_stud_exist = 0
st_for_transf_id = get_num("Введите ID студента, которого будем переводить")
for _ in my_univer.faculties:
    st_for_transf = _.get_student_by_id(st_for_transf_id)
    if st_for_transf:
        is_stud_exist = 1
        print(st_for_transf.get_student_info())
        while 1:
            new_faculty_name = input("Введите название нового факультета").capitalize()
            new_faculty = my_univer.get_faculty_by_name(new_faculty_name)
            if new_faculty:
                st_for_transf.transfer_to(new_faculty)
                print("Перевод совершен:")
                print(st_for_transf.get_student_info())
                break
            else:
                print(f"В университете {my_univer.university_name} нет факультета {new_faculty_name}")
        break
if not is_stud_exist:
    print(f"Студент с ID {st_for_transf_id} не обучается в университете {my_univer.university_name}")
