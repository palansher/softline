import timeit

my_code = """
from random import randint
test_list = [randint(1,10) for _ in range(100000)] #используем генератор списка
"""

my_code2 = """
from random import randint
my_list = []
for _ in range(100000):
    my_list.append(randint(1,10))
"""

print(timeit.timeit(my_code, number=10) / 10)
print(timeit.timeit(my_code2, number=10) / 10)