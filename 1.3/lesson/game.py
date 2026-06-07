"""Игрок может войти в казино, если у него есть сумма от 10_000. Игрок должен сделать ставку
меньше чем у него с собой сумма на то, что сможет за 3 попытки угадать загаданное число.
Если угадает, то к его сумме прибавим ставку, а если нет, то вычтем ставку из его суммы."""

from random import randint

MIN_MONEY = 10_000
MAX_TRY = 3

money = int(input('Введите сумму\n'))
if money < MIN_MONEY:
    print('Вашей суммы не хватает для начала игры')
else:
    while 1:
        rate = int(input('Введите Вашу ставку'))
        if rate <= money:
            print('Ставка принимается!')
            break
        print('Ставка не принимается, введите ставку не больше Вашей суммы!')

    # Случайное загаданное число
    NUMBER_RANDOM = randint(1, 10)
    print(NUMBER_RANDOM)

    count_try = 1
    while count_try <= MAX_TRY:
        answer = int(input(f'Попытка №{count_try}:\n'))
        if answer == NUMBER_RANDOM:
            money += rate
            print("Поздравляем, Ваша сумма стала:", money)
            break
        else:
            if count_try == MAX_TRY:
                money -= rate
                print(f"Вы проиграли, Ваша сумма = {money}, было загадано: {NUMBER_RANDOM}!")
        count_try += 1