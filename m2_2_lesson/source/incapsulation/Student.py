class Student:
    def __init__(self,first_name,course):
        self.__first_name = first_name
        self.__course = course if Student.is_course_valid(course) else 0
        self.__title = 'МГУ'

    @staticmethod
    def is_course_valid(course):
        return 1 <= course <= 5
    @property
    def first_name(self):
        return self.__first_name

    @property
    def course(self):
        return self.__course

    @course.setter
    def course(self,value):
        if Student.is_course_valid(value):
            self.__course = value

    def show_info(self):
        if self.course == 0:
            print('Курс указан некорректно')
        else:
            print(f'{self.first_name} учится в {self.__title} на {self.course}')

student = Student('Иван',4)
student.show_info()

student.course += 1
student.show_info()