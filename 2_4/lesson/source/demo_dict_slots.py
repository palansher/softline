# Все свойства объекта и свойства класса хранятся в словаре __dict__

# Если мы хотим ограничить объект только определенными свойствами, то используйте
# __slots__, т.к. то, что укажем в slots, только эти свойства объекта и могут существовать
class Car:
    # __slots__ = ('title','price')
    city = 'Москва'
    # show = True
    def __init__(self,title,price):
        self.title = title
        self.price = price
        # self.id = 1

    def show(self):
        print(self.title,self.price)

car = Car("Audi",1000)
# car.engine = 'бензиновый'
#
# setattr(car,'id',1)
# if hasattr(car,'id'):
#     print(car.id)


# print(car.__dict__)
# print(Car.__dict__)

# Проверка на наличие в классе метода show

# print(Car.__dict__)

# if 'show' in Car.__dict__ and callable(Car.__dict__['show']):
#     print('Метод show существует!')

x = {'a':1,'b':2}
# print(x['c'])#ошибка, т.к. не существует ключа c

value = x.get('c',10)
print(value)