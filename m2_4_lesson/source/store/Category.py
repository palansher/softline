class Category:
    count = 0
    def __init__(self, name):
        self.title_category = name
        Category.count += 1
        self.id = Category.count