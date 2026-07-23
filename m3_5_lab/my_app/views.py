from django.http import HttpResponse
from django.shortcuts import render, redirect
from my_app.forms import UserForm, ArticleForm

# Create your views here.


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
        # принимаем данные из формы
        form = ArticleForm(request.POST)
        # сохраняем в базе
        form.save()
        return redirect('success')
    form = ArticleForm()
    return render(request,'advanced_form.html',{'form':form})

def success(request):
    return HttpResponse('<h1>Данные сохранены в базе!</h1>')