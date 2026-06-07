class Car:
    def __init__(self,title,price):
        self.title = title
        self.price = price

    def get_info(self):
        return f"Автомобиль {self.title} стоит {self.price}"

    def add_discaunt(self,size):
        self.price -= size