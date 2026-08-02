import random

# Для получения рандомных чисел используйте основные функции
# 1) randint(a,b) - получение случайного целого числа в отрезке [a,b]
# 2) random() - получение случайного числа в отрезке [0,1)

# print(random.randint(1,10))
# print(random.random())

# Если необходимо получить вещественное случайное число в отрезке [a,b)
# используйте формулу: math.random() * (b - a) + a


# print(random.random() * 9 + 1) [1,10)
# print(random.random() * 10) #[0,10)

# [-5,20)

# print(random.random() * (20 + 5) - 5)

# cities = ['Москва','Омск','Томск'] #список элементов (массив)
# print(random.choice(cities)) #получаем случайное значение из списка значений

# print(random.randrange(0,10,3)) #0 3 6 9

# Пример - пусть есть 3 случайных возраста. Нужно вывести возраста по возрастанию

MIN_AGE = 20
MAX_AGE = 50
age1,age2,age3 = (random.randint(MIN_AGE, MAX_AGE),
                  random.randint(MIN_AGE, MAX_AGE),
                  random.randint(MIN_AGE, MAX_AGE))

# Способ №1
# print(age1,age2,age3)
#
# min_age  = min(age1,age2,age3)
# max_age = max(age1,age2,age3)
# middle_age = age1 + age2 + age3 - min_age - max_age
#
# print(min_age,middle_age,max_age)

# Способ №2
ages = [age1,age2,age3]
ages.sort()
# print(ages)

print(sorted(ages))

# Функция это универсальная команда, т.е. она не зависит от объекта
# Метод - это команда, которая применяется к объекту
