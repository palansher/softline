import datetime

current_time = datetime.datetime.now()  # noqa: DTZ005

# Интервал можно прибавить к ней, а можно отнять от нее.
# Например, какая дата будет через пятьдесят дней, пять часов и одну минуту?

delta = datetime.timedelta( #настройка интервала, который применим к дате
    days = 50,
    hours = 5,
    minutes = 1
)

new_time = current_time + delta
print(new_time)
