import datetime

from django.http import HttpResponse
from django.shortcuts import render

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
