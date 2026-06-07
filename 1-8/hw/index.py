"""
Заменить в текстовом документе все одинарные кавычки на двойные кавычки
"""


input_filename = 'input.txt'
output_filename = 'output.txt'

try:
    # Открываем исходный файл для чтения ('r')
    with open(input_filename, 'r', encoding='utf-8') as infile:
        content = infile.read()

    # Заменяем одинарные кавычки на двойные
    new_content = content.replace("'", '"')

    # Сохраняем результат в другой файл ('w')
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        outfile.write(new_content)

    print(f"Готово! Результат сохранен в файл {output_filename}")

except FileNotFoundError:
    print(f"Ошибка: Файл '{input_filename}' не найден. Проверьте путь к файлу.")
except PermissionError:
    print(f"Ошибка: Нет прав для доступа к файлу.")
except Exception as e:
    print(f"Произошла непредвиденная ошибка: {e}")
