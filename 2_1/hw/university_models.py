"""
привел имена методов к штатному питоновскому стилю
Нормально ли сейчас оформлены функции ?
"""

# Чтобы избежать ошибки, когда в процессе выполнения объект еще не декларирован. Типа свежая фича питона.
# Позволяет использовать имя класса внутри самого этого класса или до того, как он объявлен
from __future__ import annotations

# Type Hinting - для красоты, чтобы линтер не ругался, хотя и так работает
from typing import List, Optional


class Faculty:
    """Класс факультет университета."""
    _id_counter: int = 1

    def __init__(self, faculty_name: str):
        """
        Инициализация объекта факультета.
        :param faculty_name: Название факультета.
        """
        self.faculty_id: int = Faculty._id_counter
        Faculty._id_counter += 1
        self.faculty_name: str = faculty_name
        self.students: List[Student] = []

    def add_student(self, student: Student) -> None:
        """Добавляет студента в список факультета."""
        if student not in self.students:
            self.students.append(student)

    def remove_student(self, student: Student) -> None:
        """Удаляет студента из списка факультета."""
        if student in self.students:
            self.students.remove(student)

    def get_student_by_id(self, student_id: int) -> Optional[Student]:
        """
        Возвращает студента по уникальному ID.
        :param student_id: Идентификатор студента.
        :return: Объект Student или None, если не найден.
        """
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None


class Student:
    """Класс студента."""
    _id_counter: int = 1001

    def __init__(self, full_name: str, faculty: Faculty):
        """
        Инициализация студента.
        :param full_name: ФИО студента.
        :param faculty: Объект факультета.
        """
        self.student_id: int = Student._id_counter
        Student._id_counter += 1
        self.full_name: str = full_name
        self.faculty: Faculty = faculty
        self.faculty.add_student(self)

    def transfer_to(self, new_faculty: Faculty) -> None:
        """
        Переводит студента на новый факультет.
        :param new_faculty: Объект нового факультета.
        """
        if self.faculty == new_faculty:
            print(f"Ошибка: {self.full_name} уже на факультете {new_faculty.faculty_name}.")
            return

        old_faculty=self.faculty
        self.faculty.remove_student(self)
        self.faculty = new_faculty
        new_faculty.add_student(self)
        print(f"Успех: {self.full_name} переведен из {old_faculty.faculty_name} в {new_faculty.faculty_name}.")

    def get_student_info(self) -> str:
        """Возвращает строку с полной информацией о студенте."""
        return (f"Студент: [{self.full_name}] (ID: {self.student_id}), "
                f"Факультет: [{self.faculty.faculty_name}]")


class University:
    """Класс для университета"""

    def __init__(self, university_name: str):
        """
        Инициализация университета.
        :param university_name: Название университета
        """
        self.university_name: str = university_name
        self.faculties: List[Faculty] = []

    def add_faculty(self, faculty: Faculty) -> None:
        """Добавляет факультет в университет"""
        if faculty not in self.faculties:
            self.faculties.append(faculty)

    def get_faculty_by_name(self, name: str) -> Optional[Faculty]:
        """
        Возвращает факультет по названию
        :param name: Название факультета для поиска
        :return: Объект Faculty или None
        """
        for faculty in self.faculties:
            if faculty.faculty_name == name:
                return faculty
        return None

    def get_all_students(self) -> List[Student]:
        """Собирает список всех студентов университета"""
        all_students: List[Student] = []
        for faculty in self.faculties:
            all_students.extend(faculty.students)
        return all_students

    def print_all_students(self) -> None:
        """ Выводит информацию обо всех студентах """
        for student in self.get_all_students():
            print(student.get_student_info())