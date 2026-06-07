from Car import Car

# Если в классе базовом был конструктор с параметрами, то если класс потомок имеет дополнительные свойства,
# то всегда делаем в потомке тоже конструктор и в созданном конструкторе запускаем базвый конструктор.
# Запускаем конструктор либо через имя базового класса, либо через super()

class RaceCar(Car):
    def __init__(self,title,price,speed):
        super().__init__(title,price)
        self.speed = speed

    def get_info(self):
        super().add_discaunt(1000)
        info = super().get_info()
        return f"{info}\nГоночный Автомобиль {self.title} разгоняется до скорости {self.speed}"