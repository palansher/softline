from datetime import datetime
import os
import shutil


# Текущая директория
# print(os.getcwd())

# print(r'D:\Работа\2026\Март\Python middle\Урок №7')
# Смена текущей директории
# os.chdir(r'D:\Работа\2026\Март\Python middle\Урок №7')
# print(os.getcwd())

# Создание новой директории

# os.makedirs(r"C:\2\test", exist_ok=True)

# Удаление директории

# os.rmdir(r"C:\2\test")

# Для проверок на файл и папку есть специальные функции:

# print(os.path.isdir('C:/2/demo/test.txt'))
# print(os.path.isfile('C:/2/demo/test.txt'))

# full_path = os.path.join(r'C:\2','demo','test.txt')
# print(full_path)

# Поиск всех текстовых документов на диске D:

# MY_DIR = 'D:/'
# content = os.listdir(MY_DIR)
# text_files = []
# for item in content:
#     if os.path.isfile(os.path.join(MY_DIR, item)) and item.endswith(".txt"):
#         text_files.append(item)
# print(text_files)

# 1)Использование переменных окружения

# Получение значения из системной переменной
# print(os.getenv('OS'))

# 2) Запуск процессов

# os.system('notepad')

# Получение информации о системе

# print(os.getlogin())
# print(os.path.getsize(r'D:\Работа\2026\Март\Python middle\Урок №6\Урок №6.zip'))

# 3) Обход директорий
# for root,dirs,files in os.walk('D:/Работа/2026'):
#     print('Текущая директория',root)
#     print('Поддиректория',dirs)
#     print('Файлы',files)
#
#     print("*"*40)

# Создание бэкапа

def create_dump(from_source,to_source):
    if not os.path.exists(to_source):
        os.makedirs(to_source)
    path = os.path.join(to_source,f"{datetime.now().strftime('%d_%m_%Y %H_%M_%S')}")
    shutil.copytree(from_source, path)
    print(f"Бэкап создан!")

create_dump(r"D:\Работа\2026\Март\Python-I\Урок №1\Исходники урока",r"C:\2\backup")

# Удаление папки вместе с содержимым:
# shutil.rmtree("Путь к удаляемой папке")
# shutil.copy() - копирование без метаданных
# shutil.copy2() - копирование с метаданными