# Счетчик строк
num_str = 1
while num_str <= 100:
    # Счетчик ячеек для текущей строки
    num_field = 1
    while num_field <= 10:
        print(f"{num_str * num_field}\t\t",end="")
        num_field = num_field + 1
    print()
    num_str += 1