from order import Order


class Dealer(object):

    # сколько лет на рынке продает наши авто

    age = 0

    def __init__(self, title_diller, age):

        self.title_diller = title_diller

        self.age = age

    def create_order(self, order: Order):
        """

        Создание заказа

        :param order_info: Объект класса

        :return:
        """

        if self.age > 10:
            order.discount_percent = 10

        order.start()  # запуск производства

        order.show_result()
