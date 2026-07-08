from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
#from connect_db import connection
from django.contrib.auth import login, authenticate
from .models import *
from .forms import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
# Create your views here.

def add_item(request):
    Item.objects.bulk_create([
        Item(item_id = 1,title = 'ADAR 2-15',price = 1500,info = 'В наличии',photo = 'ar.jpg'),
        Item(item_id=2, title='Fabarm XLR', price=1300, info='Под заказ', photo='fabarm.jpg'),
        Item(item_id=3, title='Fantom 9P.A', price=900, info='В наличии', photo='fantom.jpg'),
        Item(item_id=4, title='Патроны 5,45х39', price=10, info='В наличии', photo='545.jpg'),
        Item(item_id=5, title='Порох ТК', price=100, info='В наличии', photo='powder.jpg'),
        Item(item_id=6, title='Прицел VectorOptics', price=500, info='В наличии', photo='optic.jpg'),
    ])
    return HttpResponse('table created')

def add_user(request):
    passwd1 = make_password('admin1')
    passwd2 = make_password('user1')
    User.objects.bulk_create([
        #админ создан python manage.py createsuperuser admin admin1
        User(id = 1,username = 'admin',password = passwd1,is_superuser = True, is_staff = True),
        User(id = 2,username = 'user',password = passwd2),
    ])
    return HttpResponse('table created')

def index(request):
    return render(request,'index.html')


def contacts(request):
    return render(request,'contacts.html')

def catalog(request):
    items = Item.objects.all().values()
    return render(request,'catalog.html',{'items':items})

def item(request, item_id):
    if request.user.is_authenticated:  # Проверка, что юзер залогинен
        user_id = request.user.id
        return render(request,'item.html',{'item':Item.objects.get(item_id=item_id), 'user':user_id})
    return render(request,'item.html',{'item':Item.objects.get(item_id=item_id), 'user':None})

def add_cart(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        if request.user.is_authenticated:
            user_id = request.user.id
        else:
            user_id = 0
        if id.isdigit():
            id = int(id)
            item = Cart.objects.filter(item_id=id).first()
            if item:
                item.quantity = item.quantity + 1
                item.save()
            else:
                Cart.objects.create(item_id=id, quantity=1, user_id=user_id)
            return redirect('/cart', code=302)
    return 'Ошибка!'


def cart(request):
    if request.user.is_authenticated:  # Проверка, что юзер залогинен
        user_id = request.user.id
        user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = OrdersForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user_id = User.objects.filter(username=order.user_name).values_list('id', flat=True).first()
            order.save()
            return redirect('/cart', code=302)
    form = OrdersForm()
    if request.user.is_authenticated:  # Проверка, что юзер залогинен
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        data = Cart.objects.raw('SELECT c.id,title,price,quantity FROM my_app_item i INNER JOIN my_app_cart c ON i.item_id=c.item_id WHERE c.user_id=%s',(user_id,))
        return render(request,'cart.html',{'items':data, 'form':form, 'user':user})
    return render(request,'cart.html',{'form':form, 'user':None})

def admin(request):
    data = Cart.objects.raw('SELECT o.user_name,user_phone, c.id,title,price,quantity FROM my_app_orders o INNER JOIN my_app_cart c ON o.user_id=c.user_id INNER JOIN my_app_item i ON i.item_id=c.item_id')
    return render(request,'admin.html', {'items':data})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()          # Сохраняем нового пользователя
            login(request, user)        # Выполняем вход
            return redirect('catalog')     # Перенаправляем на главную страницу
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password) # Проверяем учетные данные
            if user is not None:
                login(request, user)
                if request.user.is_superuser:
                    return redirect('admin/')
                else:
                    return redirect('cart/')
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')