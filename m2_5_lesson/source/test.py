import abc


class A(abc.ABC):
    @abc.abstractmethod
    def show(self):
        pass

class B(A):
    def show(self,a):
        print(f"{a} = {a}")


B().show(1)