# Если необходимо доступ к свойству объекта закрыть - используйте "__" перед название свойства
#
# Геттеры - это методы, которые возвращают значения свойств объекта. То есть можно всегда
# делать геттеры для каждого свойства. То есть методы, которые предоставляют доступ к объекту
# в режиме чтения

# Сеттеры - это методы, которые предоставляют доступ к свойству объекта в режиме записи

class Person:
    pasword = "123"

    def __init__(self,name,salary):
        self.__name = name
        self.__salary = salary

    def set_salary(self,salary):
        if input('Введите пароль для изменения оклада') == Person.pasword:
            self.__salary = salary
            return
        print("Нет доступа!")

    def set_name(self,name):
        self.__name = name

    def get_name(self):
        return self.__name

    def get_salary(self):
        return self.__salary

    def __str__(self):
        return self.__name + ' получает оклад ' + str(self.__salary)

man = Person("Вася",100_000)
# man.__salary += 100_000

print(man.get_salary())
man.set_salary(300_000)
print(man.get_salary())

# print(man._Person__salary)