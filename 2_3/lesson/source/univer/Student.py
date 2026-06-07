
class Student:
    count = 0
    def __init__(self,full_name,faculty):
        Student.count += 1
        self.full_name = full_name
        self.faculty = faculty
        self.student_id = Student.count

    def get_student_info(self):
        return f"Студент: [{self.full_name}] (ID: {self.student_id}), Факультет: {self.faculty.title_faculty}"

    # def is_exist_faculty(self,univer,faculty)->bool:
    #    for faculty in univer.faculties:
    #        if faculty.title_faculty == faculty.title_faculty:
    #            return True
    #    return False

    def transfer_to(self,newFaculty):
        """Переводим студента на новый факультет"""
        self.faculty.remove_student(self)
        self.faculty = newFaculty
        self.faculty.students.append(self) #добавили студента в новый факультет

