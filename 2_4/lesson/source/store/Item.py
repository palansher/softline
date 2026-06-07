class Item:
    count = 0
    def __init__(self, title, price,category):
        self.category = category
        self.title = title
        self.price = price
        Item.count += 1
        self.id = Item.count