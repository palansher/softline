import datetime
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render


# Create your views here.
def index(request):
    return HttpResponse("<h1>Добрый день!</h1>")


# http://127.0.0.1:8000/pass_data?name=Ivan&age=25
def pass_data(request):
    # Задаем дефолтное имя, если его нет
    name = request.GET.get("name", "Гость")
    age = request.GET.get("age")

    if age and age.isdigit():
        age = int(age)
        current_year = datetime.datetime.now().year
        return HttpResponse(
            f"Добрый день, {name}! Ваш год рождения {current_year - age}"
        )

    # Если age не передан или это не число, возвращаем понятную Django ошибку (код 400)
    return HttpResponseBadRequest("Ошибка! Неверно указан возраст.")


def pass_data_v2(request, name, age):
    return HttpResponse(
        f"Добрый день, {name}, Ваш год рождения: {datetime.datetime.now().year - int(age)}"
    )


"""Создать 3 параметра - 2 числа и один знак операции. Вывести в формате 2 + 2 = 4"""


def calc(request, a, b, sign):
    if sign == "+":
        return HttpResponse(f"{a} {sign} {b} = {a + b}")
    elif sign == "-":
        return HttpResponse(f"{a} {sign} {b} = {a - b}")
    elif sign == "*":
        return HttpResponse(f"{a} {sign} {b} = {a * b}")
    elif sign == "/":
        if b == 0:
            return HttpResponse("Ошибка: деление на ноль!")
        return HttpResponse(f"{a} {sign} {b} = {a / b}")
    else:
        return HttpResponse("Неизвестная операция")


def test_template(request):
    data = {"name": "Иван", "age": 18}
    return render(request, "info.html", data)


def form(request):
    return render(request, "form.html")


def get_data_from_form(request):
    if request.method == "POST":
        a = request.POST.get("a", 0)
        b = request.POST.get("b", 0)
        if a.isdigit() and b.isdigit():
            a = float(a)
            b = float(b)
            sign = request.POST.get("sign", "+")
            expression = f"{a} {sign} {b}"
            res = round(eval(expression), 2)
            return render(
                request, "form.html", {"a": a, "b": b, "res": res, "sign": sign}
            )
    return HttpResponseBadRequest("Ошибка!")


def demo_ajax(request):
    if request.method == "POST":
        a = request.POST.get("a", 0)
        b = request.POST.get("b", 0)
        if a.isdigit() and b.isdigit():
            a = float(a)
            b = float(b)
            return HttpResponse(f"{a} + {b} = {a + b}")
    return render(request, "demo_ajax.html")
