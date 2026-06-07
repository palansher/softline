from Order import Order
class Diler:
    def __init__(self,title_diler,age):
        self.title_diler = title_diler
        self.age = age


    def create_order(self,order:Order):
        order.start_order(self.age)
        order.show_result()
