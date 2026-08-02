# # Для работы с текстовыми документами сначала файл открываем и указываем с какой целью его открываем.
# # Функция open(путь к файлу, режим открытия файла)
# # Режимы:
# # r - для чтения
# # w - для записи (если файла не существует, при этом режиме он создается)
# # a - дополняем файл новым контентом
#
# # file = open("demo.txt","a")
#
# # Для записи данных в файл используйте две функции:
# # 1) file.write("Строка") - записываем строку в файл
# # 2) file.writelines(Список строк) - каждый элемент списка запишется как отдельная строка в файле
#
# # file.write("111\n222\n333\n")
# # file.writelines(["444\n","555"])
#
#
# # Чтение данных из файла
#
# # Основные методы:
# # 1) read - считываем весь файл в виде одной строки
# # 2) readline - считываем первую строку файла
# # 3) readlines - считываем все строки файла в виде списка строк
#
# with open("demo.txt","r") as f:
#     # Пример №1
#     # for line in f:
#     #     print(line,end="")
#
#     # Пример №2
#     # content = [line.strip('\n') for line in f.readlines()]
#     # print(content)
#
#     # Пример №3
#     print(f.read())


# 1) Вывести матрицу в консоль в исходном виде
# 2) Вывести матрицу в консоль таким образом, чтобы каждая строка матрицы
# была возведена в степень равную номеру строки

def read_matrix_advanced():
    exp = 0
    with open("matrix.txt", "r") as f:
        for line in f:
            if line != "\n":
                exp += 1
                numbers = line.split(" ")
                for number in numbers:
                    print(int(number) ** exp,end=" ")
                print()
# read_matrix_advanced()


# with open("matrix.txt", "r") as f:
#     for i, line in enumerate(f.readlines()):
#         for char in line:
#             if char in '0123456789':
#                 ichar = int(char)
#                 print(ichar ** (i+1), end=" ")
#         print()