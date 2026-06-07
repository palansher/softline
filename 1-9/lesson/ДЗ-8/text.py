"""Заменить в текстовом документе все одинарные кавычки на двойные кавычки"""

# Создаем файл txt
# file = open("text.txt","a")
#
# file.writelines(["'text_1'\n","'text_2'\n", "'text_3'\n", "'text_4'\n"])

# 1-й вариант

# Открываем файл и считываем весь текст
with open("text.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Создаём пустую строку для нового текста
new_text = ""

# Проходим по каждому символу и заменяем одинарные кавычки на двойные
for symbol in text:
    if symbol == "'":
        new_text += '"'
    else:
        new_text += symbol

# Открываем файл для записи и сохраняем изменённый текст
with open("text.txt", "w", encoding="utf-8") as f:
    f.write(new_text)

# 2-й вариант

# # Открываем файл и считываем весь текст
# with open("text.txt", "r", encoding="utf-8") as f:
#     text = f.read()
#
# # Заменяем все одинарные кавычки на двойные
# text = text.replace("'", '"')
#
# # Открываем файл для записи и сохраняем измененный текст
# with open("text.txt", "w", encoding="utf-8") as f:
#     f.write(text)