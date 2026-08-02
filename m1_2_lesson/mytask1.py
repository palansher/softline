"""
Есть рандомная стоимость товара от 300 руб до 2000руб. Если стоимость товара выше 500 руб,
то скидка 5%, а если стоимость товара выше 1000руб, то скидка 10%. Вывести конечную стоимость
товара с учетом скидки, если она применялась
"""

from random import randint

price = randint(300,2000)
print("Init Price: ", str(price ))
print("Price: ", price)
discount=0
if price > 1000:
    price *= 0.9
elif price >500:
    price *= 0,95

print("Final Price: ", str(price ))
