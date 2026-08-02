from random import randint

# color = input('Введите цвет, который сейчас горит у светофора: red,yellow,green')

# if color == 'red':
#     print('Стоп')
# elif color == 'yellow':
#     print('Внимание')
# elif color == 'green':
#     print('Вперед')
# else:
#     print('Поломка светофора')

# match color:
#     case 'red':
#         print('Стоп')
#     case 'yellow':
#         print('Внимание')
#     case 'green':
#         print('Вперед')
#     case _:
#         print('Поломка светофора')

# Пример: Вычислить стоимость разговора по телефону с учетом того, что в выходные скидка на разговор с каждой минуты 20%
# Использовать match/case

# Дано:
# 1) Продолжительность разговора в минутах
# 2) Стоимость разговора за 1 минуту
# 3) День недели

count_minutes = input('Введите количество минут')
if count_minutes.isdigit():
    count_minutes = int(count_minutes)
    # Стоимость разговора за 1 минуту
    PRICE = 5
    day = input('Введите день недели в любом удобном Вам формате').lower()
    match day:
        case 'воскресенье' | '7' | 'суббота' | '6':
            print('Предоставляется скидка!')
            DISCAUNT = 20
        case _:
            DISCAUNT = 0
    result_price = count_minutes * PRICE
    # if DISCAUNT > 0:
    #     result_price -= result_price * DISCAUNT / 100
    # print(DISCAUNT)
    result_price = count_minutes * PRICE if DISCAUNT == 0 else result_price - (result_price * DISCAUNT / 100)

    print(result_price)


# if True:
#     x = 1
# print(x)