"""
Задание 1.4
"""

# Напишите функцию get_middle(start, end), которая находит среднее
# арифметическое значение в отрезке от start до end

def get_middle(start, end):
    summa, total = 0, 0
    for i in range(start, end+1):
        summa += i
        total += 1
    return summa/total

a = int(input("Введите start: "))
b = int(input("Введите end: "))
print(f"Среднеарифметическое значение = {get_middle(a, b)}")

# С клавиатуры вводятся N чисел. Составьте программу, которая
# определяет количество отрицательных, количество положительных
# и количество нулей среди введенных чисел. Значение N вводится с
# клавиатуры. При вводе нечислового значения вывести сообщение
# об ошибке и просим ввести повторно именно числовое значение.
# Используйте цикл for.

while (1):
    n = input("Введите N\n")
    if (n.isdigit()) and (int(n) > 0):
        break
    print("Введите положительное число!")
# Переменные для подсчета
plus, minus, zero = 0, 0, 0
for i in range(1, int(n)+1):
    while (1):
        num = input(f'Введите {i}-e число: ')
        if len(num) > 0:
            if (len(num) == 1 and num.isdigit()) or (num[0] == "-" and num[1:].isdigit()) or (num.isdigit()):
                if int(num) > 0:
                    plus += 1
                elif int(num) < 0:
                    minus += 1
                else:
                    zero += 1
                break
            else:
                print("Вы ввели не цифру! Повторите ввод.")
        else:
            print("Вы не ввели ничего! Повторите ввод.")
print(f"Количество положительных цифр = {plus}\n"
      f"Количество отрицательных цифр = {minus}\n"
      f"Количество цифр, равных нулю = {zero}\n")