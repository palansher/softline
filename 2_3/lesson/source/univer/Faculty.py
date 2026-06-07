from univer.Student import Student


class Faculty:
    count = 0
    def __init__(self,title_faculty:str)->None:
        Faculty.count += 1
        self.faculty_id = Faculty.count
        self.title_faculty = title_faculty
        self.students = []

    def add_student(self):
        """Добавление студента на факультет"""
        fio = input("Введите ФИО")
        student = Student(fio,self)
        self.students.append(student)
        print(f"Студент (ID = {student.student_id}): {student.full_name} зачислен на факультет {self.title_faculty}")


    def remove_student(self,student):
        """Удаление студента с факультета"""
        if student in self.students:
            student.faculty = None
            self.students.remove(student)

    def get_student_by_id(self,student_id:int)->Student:
        for student in self.students:
            if student.student_id == student_id:
                return student