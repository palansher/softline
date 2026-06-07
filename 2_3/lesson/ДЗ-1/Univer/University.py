"""
University - Created on 11.10.2025 11:16
Класс University (Университет)
"""


class University:
    def __init__(self, university_name):
        self.university_name = university_name
        self.faculties = []

    def add_faculty(self, faculty):
        """добавляет факультет в университет"""
        self.faculties.append(faculty)
        print(f"В университете {self.university_name} создан факультет {faculty.faculty_name}")

    def get_faculty_by_name(self, faculty_name_text):
        """возвращает факультет по названию"""
        for faculty in self.faculties:
            if faculty.faculty_name == faculty_name_text:
                return faculty

    def get_all_students(self):
        """возвращает список всех студентов университета"""
        print("*" * 50)
        print(f"Студенты университета {self.university_name}:")
        print("-" * 50)
        for _ in self.faculties:
            if len(_.students) == 0:
                print(f"На факультете {_.faculty_name} студентов сейчас нет")
                print("-" * 50)
            else:
                for st in _.students:
                    print(st.get_student_info())
                print("-" * 50)
                print(f"Всего на факультете {_.faculty_name} обучается студентов: {len(_.students)}")
                print("-" * 50)
