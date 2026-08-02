"""
Student - Created on 11.10.2025 11:17
Класс Student (Студент)
"""


class Student:
    count = 0

    def __init__(self, full_name, faculty):
        Student.count += 1
        self.student_id = Student.count
        self.full_name = full_name
        self.faculty = faculty

    def get_student_info(self):
        """возвращает строку с полной информацией о студенте"""
        return f"Студент: {self.full_name} (ID={self.student_id}), Факультет: {self.faculty.faculty_name}"

    def transfer_to(self, new_faculty):
        """переводит студента на новый факультет"""
        self.faculty.remove_student(self)
        self.faculty = new_faculty
        self.faculty.students.append(self)
