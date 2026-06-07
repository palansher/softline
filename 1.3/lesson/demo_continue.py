# Для принудительной остановки текущей итерации цикла используйте оператор continue
# Пропустим столбец №5


# Счетчик строк
num_str = 1
# Цикл по строкам
while num_str <= 100:
    # Счетчик ячеек для текущей строки
    num_field = 1
    # Цикл по столбцам
    while num_field <= 10:
        if num_field == 5:
            num_field = num_field + 1
            continue
        print(f"{num_str * num_field}\t\t",end="")
        num_field = num_field + 1
    print()
    num_str += 1
print("Инструкции после вывода таблицы...")