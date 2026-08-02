class Car:
    wheels = 4
    def __init__(self, mark):
        self.mark = mark

car1 = Car("Audi")
car2 = Car("BMW")

car1.wheels = 6
car1.sgdg = 22

Car.wheels = 10

print(car1.sgdg)