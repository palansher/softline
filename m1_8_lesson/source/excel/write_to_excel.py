import numbers

from openpyxl import Workbook

book = Workbook()

my_list = book.active

my_list['A1'] = "Audi"
my_list['B1'] = 1000
my_list['B1'].number_format = numbers.FORMAT_NUMBER


my_list['A2'] = "BMW"
my_list['B2'] = 1200

book.save('cars.xlsx')