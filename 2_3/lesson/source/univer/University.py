"""Класс Университет"""
from Faculty import Faculty


class University:
    def __init__(self,title_univer:str)->None:
        self.title_univer = title_univer
        self.faculties = []

    def add_faculty(self,faculty:Faculty):
        """Добавление факультета в университет"""
        self.faculties.append(faculty)
        print(f"В университете {self.title_univer} создан факультет {faculty.title_faculty}")

    def get_faculty_by_title(self,title_faculty:str)->Faculty:
        """Возвращаем факультет по названию"""
        for faculty in self.faculties:
            if faculty.title_faculty == title_faculty:
                return faculty

    def get_all_students(self):
        """Вернем список всех студентов со всех факультетов"""
        print("*" * 50)
        print("Студенты университета ",self.title_univer,":",sep="")
        for faculty in self.faculties:
            if len(faculty.students) == 0:
                print(f"На факультете {faculty.title_faculty} студентов сейчас нет")
                print("-" * 50)
            else:
                for student in faculty.students:
                    print(student.get_student_info())
                print("*" * 50)
                print(f"Всего на факультете {faculty.title_faculty} обучается студентов {len(faculty.students)}")
                print("*" * 50)