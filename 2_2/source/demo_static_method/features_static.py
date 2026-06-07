class Demo:
    def __init__(self):
        self.x = 0
    def f(self):
        self.x += 1
        print(self.x)

obj1 = Demo()
obj2 = Demo()

obj1.f()
obj1.f()

obj2.f()
obj2.f()