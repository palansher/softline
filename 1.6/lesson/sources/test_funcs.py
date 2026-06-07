n = [1,2,3,4,5,6]

# Вариант №1
# new_items = [i for i in n if i % 2 == 0]

# Вариант №2
# new_items = []
# for i in n:
#     if i % 2 == 0:
#         new_items.append(i)

# Вариант №3
# print(list(filter(lambda item : item % 2 == 0,n)))
#
# print(n)

list_celsia = [-10,25,15]

list_farenheit = list(map(lambda x: 9 * (x - 32) / 5, list_celsia))
print(list_farenheit)

