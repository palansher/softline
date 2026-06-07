class Pizza:
    def __init__(self,title,ingredients):
        self.title = title
        self.ingredients = ingredients

    # Создаем метод, который будет возвращать новый объект текущего класса
    @classmethod
    def create_pizza(cls,title_pizza):
        match title_pizza:
            case "Маргарита":
                return cls('Маргарита',['Сыр','Томатный соус'])
            case "Пицца с грибами":
                return cls('Грибная',['Грибы','Сыр'])

    def show_pizza(self):
        print(self.title,'содержит ингредиенты',self.ingredients)


pizza1 = Pizza.create_pizza('Маргарита')
pizza1.show_pizza()

pizza2 = Pizza.create_pizza('Пицца с грибами')
pizza2.show_pizza()