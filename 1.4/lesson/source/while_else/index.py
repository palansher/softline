# Поиск символа в строке не используя строковых методов и оператор in

# 1ый способ решения

# str = "hello world!"
# find = input("Введите символ\n")
# # Пусть по умолчанию мы предположим, что символ не существует в строке
# is_found = False
# i = 0
# while i < len(str):
#     if str[i] == find:
#         is_found = True
#         print("Символ найден!")
#         break
#     i += 1
# if not is_found:
#     print("Элемент не найден!")


# Способ №2 (while/else)
# Конструкция while/else означает, что если в цикле while был вызван оператор break, то выражение
# после else не выполняется, а если break не был вызван, то выражение после else будет выполняться

str = "hello world!"
find = input("Введите символ\n")
i = 0
while i < len(str):
    if str[i] == find:
        print("Символ найден!")
        break
    i += 1
else:
    print("Элемент не найден")