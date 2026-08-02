class Car:

    def __init__(self, title, base_price):
        self.title = title
        
        # базовая цена
        self.base_price = base_price
        
        # отпускная цена для дилера
        self.sell_price = base_price
