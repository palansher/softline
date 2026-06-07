# Создаем университет
import random

from univer.Faculty import Faculty
from univer.Student import Student
from univer.University import University

my_univer = University("МГУ")

my_univer.add_faculty(Faculty("МЕХ-МАТ"))
my_univer.add_faculty(Faculty("ФИЗ-МАТ"))
my_univer.add_faculty(Faculty("КНиИТ"))

# Зачисляем студентов

print(f"Зачисляем в университет {my_univer.title_univer} 5 студентов")

for _ in range(5):
    random.choice(my_univer.faculties).add_student()

my_univer.get_all_students()

# Переводим студента на другой факультет

print("*" * 50)
student_id = int(input('Введите ID студента, которого будем переводить\n'))
student_for_transfer = None

for faculty in my_univer.faculties:
    student_for_transfer = faculty.get_student_by_id(student_id)
    if student_for_transfer:
        break

if student_for_transfer:
    print(student_for_transfer.get_student_info())
    while True:
        new_faculty_title = input('Введите название нового факультета: ').upper()
        new_faculty = my_univer.get_faculty_by_title(new_faculty_title)
        if new_faculty:
            student_for_transfer.transfer_to(new_faculty)
            print("Перевод студента осуществлен!")
            print(student_for_transfer.get_student_info())
            break
        else:
            print("Вы ввели несуществующий факультет")
else:
    print("Введенный студент не обучается в Вузе!")