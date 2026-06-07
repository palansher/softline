from Order import Order


class Diller:
    def __init__(self,title_diller,age):
        self.title_diller = title_diller
        self.age = age

    def create_order(self,order:Order)->None:
        """Создание заказа на основе документа
         :param order_doc: объект класса Order, который
         содержит всю информацию о заказе
        """""
        # запуск производства. Цель - отправить на завод фуру для погрузки в нее автомобилей
        order.start()
        order.show_result()