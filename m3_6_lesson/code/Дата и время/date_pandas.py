# Пример №1
# Создаем диапазон дат с 1 июня по 30 июля
from pprint import pprint

import pandas as pd
#
# dates = pd.date_range('2026-06-01','2026-07-01')
# print(dates)

# Пример №2 (создать 20 равномерно распределенных дат с 1 июня до 30 июля)
dates = pd.date_range('2026-06-01','2026-07-01',periods=10)
pprint(dates)