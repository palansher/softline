s = 'Python'
bs = b'Python'

# Функция encode - преобразует строку в байты
# Функция decode - преобразует байты в строку

str = bs.decode('UTF-8') #преобразовали строку байт в строку с кодировкой UTF-8
# print(str)

# Конвертация строки в байты

bstr = s.encode('UTF-8')
print(bstr)

