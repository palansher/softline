import datetime

current_time = datetime.datetime.now()

delta = datetime.timedelta( #настройка интервала, который применим к дате
    days = 50,
    hours = 5,
    minutes = 1
)

new_time = current_time + delta
print(new_time)