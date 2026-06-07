"""Создать две рандомные переменные «a» и «b» от-10 до 10. Затем написать скрипт, который работает по
следующему принципу:
если “a” и “b” положительные, вывести их разность;
если “a” и “b” отрицательные, вывести их произведение;
если “a” и “b” разных знаков, вывести их сумму;"""

from random import randint

a = randint (-10,10)
b = randint (-10,10)
print(a,b)
if a==0 or b==0:
    print("Одно из чисел 0")
elif a>0 and b>0:
    print(a-b)
elif a<0 and b<0:
    print(a*b)
else:
    print(a+b)

# 2й способ
# a = randint (-10,10)
# b = randint (-10,10)
# print(a,b)
# if a==0 or b==0:
#     print("Одно из чисел 0")
# elif a>0 and b>0:
#     print(a-b)
# elif a<0 and b<0:
#     print(a*b)
# elif (a>0 and b<0) or (a<0 and b>0):
#     print(a + b)

