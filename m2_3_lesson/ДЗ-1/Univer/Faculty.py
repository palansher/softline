"""
Faculty - Created on 11.10.2025 11:17
Класс Faculty (Факультет)
"""
from Univer.Student import Student


class Faculty:
    count = 0

    def __init__(self, faculty_name):
        Faculty.count += 1
        self.faculty_id = Faculty.count
        self.faculty_name = faculty_name
        self.students = []

    def add_student(self):
        """добавляет студента на факультет"""
        fio = input("Введите ФИО")
        stud = Student(fio, self)
        self.students.append(stud)
        print(f"Студент (ID={stud.student_id}): {stud.full_name} зачислен на факультет {self.faculty_name}")

    def remove_student(self, student):
        """удаляет студента с факультета"""
        if student in self.students:
            student.faculty = None
            self.students.remove(student)

    def get_student_by_id(self, st_id):
        """возвращает студента по его ID"""
        for student in self.students:
            if student.student_id == st_id:
                return student
        # print(f"Студент с ID={st_id}) не обучается на факультете {self.faculty_name}")
