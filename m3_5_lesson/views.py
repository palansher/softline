from urllib.parse import quote, unquote

from django.http import HttpResponse
from django.shortcuts import render, redirect

from my_app.forms import UserForm, ArticleForm


def generate_form(request):
    if request.method == 'POST':
        name = request.POST.get('name','')
        comment = request.POST.get('comment','')
        age = request.POST.get('age','')
        return HttpResponse(f'Привет, {name}! Твой возраст: {age}!'
                            f'Комментарий: {comment}')
    user = UserForm()
    return render(request,'advanced_form.html',{'form':user})

def form_to_db(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        form.save()
        return redirect('success')
    form = ArticleForm()
    return render(request,'advanced_form.html',{'form':form})

def success(request):
    return HttpResponse('<h1>Данные сохранены в базе!</h1>')

def create_cookie(request):
    html = HttpResponse("<h1>Demo2</h1>")
    # Кодируем кириллицу в формат, понятный для HTTP (например, %D0%98...)
    name = quote('Иван')
    html.set_cookie('test_cookie2', name, max_age=None)
    return html

def use_cookie(request):
    # Получаем закодированную строку и возвращаем её в исходный вид
    encoded_name = request.COOKIES.get('test_cookie2', '')
    name = unquote(encoded_name)
    return HttpResponse('Привет, {0}'.format(name))