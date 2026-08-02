from order import Order


class Diller(object):
    def __init__(self, title_diller, age):
        self.title_diller = title_diller
        self.age = age

    def create_order(self, order: Order):
        """
        Создание заказа
        :param order_info: Объект класса
        :return:
        """

        order.start() # запуск производства
        order.show_result()