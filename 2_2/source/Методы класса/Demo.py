class Demo:
    counter =10
    def __init__(self,a):
        self.a = a

    @staticmethod
    def test():
        print(11)

    @classmethod
    def f(cls):
        print(cls.counter)
        cls.test()

    def g(self):
        print(self.a)

d = Demo(10)
Demo.g(d)