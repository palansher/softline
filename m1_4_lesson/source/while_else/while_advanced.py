# Найти сумму нечетных чисел от 0 до 50

i = s = 0
while i < 50:
    s += i if i % 2 else 0
    i += 1
print(s)

