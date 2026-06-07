# Проверка ввода ожидаемого значения

while 1:
    answer = input('Введите значение от 1 до 10')
    if not answer.isdigit():
        print('Вы ввели нечисло или отрицательное значение!')
        continue
    if 1 <= int(answer) <= 10:
        print("Принимается!")
        break
    else:
        print('Вы ввели некорректное значение!')