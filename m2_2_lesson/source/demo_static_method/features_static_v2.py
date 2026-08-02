class Demo:
    x = 0
    @staticmethod
    def f():
       Demo.x += 1
       print(Demo.x)

obj1 = Demo()
obj2 = Demo()

obj1.f()
obj1.f()

obj2.f()
obj2.f()