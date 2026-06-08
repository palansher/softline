import datetime
from curses.ascii import isdigit
from itertools import count

from django.db.models import Max, Sum
from django.http import HttpResponse
from django.shortcuts import render

from connect_db import connection
from my_app.models import Car

items = [
    {
        'id': 1,
        'title': 'Audi',
        'price': 1000,
        'info': 'Автомобиль в наличии.........',
        'img': 'audi.jpg'
    },
    {
        'id': 2,
        'title': 'BMW',
        'price': 1200,
        'info': 'Автомобиль в наличии.........',
        'img': 'bmw.jpg'
    },
    {
        'id': 3,
        'title': 'VW',
        'price': 900,
        'info': 'Автомобиль под заказ.........',
        'img': 'vw.jpg'
    },
    {
        'id': 4,
        'title': 'Skoda',
        'price': 950,
        'info': 'Автомобиль в наличии.........',
        'img': 'skoda.jpg'
    },

    {
        'id': 5,
        'title': 'Audi',
        'price': 1000,
        'info': 'Автомобиль в наличии.........',
        'img': 'audi.jpg'
    },
    {
        'id': 6,
        'title': 'BMW',
        'price': 1200,
        'info': 'Автомобиль в наличии.........',
        'img': 'bmw.jpg'
    },
    {
        'id': 7,
        'title': 'VW',
        'price': 900,
        'info': 'Автомобиль под заказ.........',
        'img': 'vw.jpg'
    },
    {
        'id': 8,
        'title': 'Skoda',
        'price': 950,
        'info': 'Автомобиль в наличии.........',
        'img': 'skoda.jpg'
    }
]
# Create your views here.
def index(request):
    return HttpResponse('<h1>Добрый день!</h1>')

def pass_data(request):
    name = request.GET.get('name')
    age = request.GET.get('age')
    if age:
        if age.isdigit():
            age = int(age)
            return HttpResponse(f'Добрый день, {name}, Ваш год рождения: {datetime.datetime.now().year - age}')
    return HttpResponse('Ошибка!!!')

def pass_data_v2(request, name,age):
    return HttpResponse(f'Добрый день, {name}, Ваш год рождения: {datetime.datetime.now().year - int(age)}')

"""Создать 3 параметра - 2 числа и один знак операции. Вывести в формате 2 + 2 = 4"""
def calc(request, a, b , sign):
    if sign == '+':
        return HttpResponse(f"{a} {sign} {b} = {a+b}")
    elif sign == '-':
        return HttpResponse(f"{a} {sign} {b} = {a-b}")
    elif sign == '*':
        return HttpResponse(f"{a} {sign} {b} = {a*b}")
    elif sign == '/':
        if b == 0:
            return HttpResponse("Ошибка: деление на ноль!")
        return HttpResponse(f"{a} {sign} {b} = {a/b}")
    else:
        return HttpResponse("Неизвестная операция")


def test_template(request):
    data = {'name':'Иван','age':18}
    return render(request,'info.html',data)

def form(request):
    return render(request,'form.html')

def get_data_from_form(request):
    if request.method == 'POST':
        a = request.POST.get('a',0)
        b = request.POST.get('b',0)
        if a.isdigit() and b.isdigit():
            a = float(a)
            b = float(b)
            sign = request.POST.get('sign','+')
            expression = f'{a} {sign} {b}'
            res = round(eval(expression),2)
            return render(request,'form.html',{'a':a,'b':b,'res':res,'sign':sign})

def demo_ajax(request):
    if request.method == 'POST':
        a = request.POST.get('a', 0)
        b = request.POST.get('b', 0)
        if a.isdigit() and b.isdigit():
            a = float(a)
            b = float(b)
            return HttpResponse(f'{a} + {b} = {a + b}')
    return render(request,'demo_ajax.html')


def demo_parse_data_in_template(request):
    cities = ['Москва','Казань','Омск']
    item = {
        'title':'Ауди',
        'price':1000,
        'color':'Белый'
    }

    cars = [
        {
            'title': 'Ауди',
            'price': 1000,
            'color': 'Белый'
        },
        {
            'title': 'БМВ',
            'price': 1200,
            'color': 'Черый'
        },
        {
            'title': 'VW',
            'price': 900,
            'color': 'Серый'
        }
    ]

    return render(request,'demo_parse.html',{'cities':cities,'item':item,'cars':cars})

def catalog(request):

    return render(request,'catalog.html',{'items':items})

def card(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        if id.isdigit():
            id = int(id)
            for item in items:
                if item['id'] == id:
                    return render(request, 'card.html', {'item': item})
    return HttpResponse("ID НЕ НАДЕН!")

def add_car(request):
    # Добавим 1 новую запись
    # Car.objects.create(name='Audi',price=1000)

    # Добавление нескольких записей
    Car.objects.bulk_create([
        Car(name='BMW', price=1200),
        Car(name='VW', price=900),
    ])
    return HttpResponse('Автомобиль создан')

def show_cars(request):
    cars = Car.objects.all() #получили список объектов
    # return HttpResponse(cars.query) #вывод запроса, который отработал

    # Получим авто БМВ
    # cars = Car.objects.all().filter(name='BMW')

    # Сортировка по алфавиту
    # cars = cars.order_by('name')

    # Сортировка против алфавита
    cars = cars.order_by('-name')
    s  = ""
    for car in cars:
        s += f"{car.name}: {car.price}<hr>"
    return HttpResponse(s)

def get_cars(request):
    # BMW = Car.objects.get(name='BMW')
    # return HttpResponse(BMW.name)

    # Агрегатные функции
    max_price = Car.objects.aggregate(Max('price'))['price__max']
    sum_price = Car.objects.aggregate(Sum('price'))['price__sum']
    count = Car.objects.count()
    return HttpResponse(f"max_price: {max_price}, sum_price: {sum_price}, count: {count}")

def simple_catalog(request):
    # cars = Car.objects.all()
    # return HttpResponse(cars[0].name)
    # Другой вариант
    cars = Car.objects.all().values()
    return render(request,'cat_simple.html',{'cars':cars})

def create_query(request):
    cars = Car.objects.raw('SELECT * FROM my_app_car WHERE price > %s ORDER BY id DESC',[1000])
    s = ""
    for car in cars:
        s += f"{car.name}: {car.price}<hr>"
    return HttpResponse(s)

def demo_update(request):
    # 1ый способ обновления
    # car = Car.objects.get(id=3)
    # car.price += 100
    # car.save()
    # return HttpResponse('Обновлено')

    # 2ой вариант
    count_records = Car.objects.filter(id=3).update(name='Porshe',price=1500)
    return HttpResponse(str(count_records))

def demo_delete(request):
    return HttpResponse(Car.objects.filter(id=30).delete())

def get_car(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        if isdigit(id):
            id = int(id)
            car = Car.objects.filter(id=id)
            return HttpResponse(car.name)
    return HttpResponse("ID не существует!")

# Создать модель для сотрудника. У сотрудника есть имя и оклад.
# Создать 3 сотрудников
# Вывести их на странице шаблона

def test_cursor(request):
    with connection.cursor() as cursor:
        cursor.execute('select * from my_app_car order by id desc')
        rows = cursor.fetchall()
        s = ""
        for row in rows:
            s += f"{row[0]}: {row[1]}<hr>"
        return HttpResponse(s)  