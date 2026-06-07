from openpyxl import Workbook

book = Workbook()

my_sheet = book.active

my_sheet['A1'] = 25
my_sheet
my_sheet['A2'] = 20
my_sheet['A3'] = '=SUM(A1:A2)'

book.save("demo.xlsx")