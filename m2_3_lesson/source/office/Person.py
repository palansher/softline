class Person:
    def __init__(self, fio:str, position):
       self.fio = fio
       self.position = position

    def get_info(self):
        return f"Сотрудник {self.fio} в должности {self.position.title} зарабатывает {self.position.calc_salary()}"