import datetime
from zoneinfo import ZoneInfo

moscow_tz = ZoneInfo("Europe/Moscow")


current_time = datetime.datetime.now(tz=moscow_tz)

# print(current_time)

# Запрашиваем у юзера дату рождения

dr = input('Введите дату своего рождения: ДД.ММ.ГГГГ: ')
date_obj = datetime.datetime.strptime(dr,"%d.%m.%Y").replace(tzinfo=moscow_tz)
# print(date_obj)

# Получим количество прожитых дней на текущую дату
count_days = (current_time - date_obj).days
print(count_days)
age = int(count_days/365)
print(age)
