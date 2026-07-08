"""Представления главного приложения — каталог, авторизация, изображения."""

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
)
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from cart.forms import CartAddProductForm

from .models import Category, Product, SiteSettings


def product_list(request):
    """Главная страница — список категорий магазина."""
    categories = Category.objects.prefetch_related('products').all()
    return render(request, 'main/product_list.html', {
        'categories': categories,
    })


def category_detail(request, slug):
    """Страница товаров выбранной категории."""
    category = get_object_or_404(Category, slug=slug)
    products = (
        Product.objects.select_related('category')
        .filter(category=category, available=True)
    )
    return render(request, 'main/category_detail.html', {
        'category': category,
        'products': products,
    })


def product_detail(request, slug):
    """Карточка отдельного товара."""
    product = get_object_or_404(Product, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'main/product_detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
    })


def product_image_db(request, product_id):
    """Загрузка изображения товара из БД."""
    product = get_object_or_404(Product, id=product_id)

    if not product.image_data:
        return HttpResponse('<h2>Нет изображения</h2>', status=404)

    # Определяем MIME-тип по magic bytes
    content_type = 'image/jpeg'  # по умолчанию
    try:
        data = bytes(product.image_data)
        if data[:4] == b'\x89PNG':
            content_type = 'image/png'
        elif data[:6] in (b'GIF87a', b'GIF89a'):
            content_type = 'image/gif'
    except (TypeError, ValueError):  
        return HttpResponse('<h2>Ошибка чтения изображения</h2>', status=404)

    return HttpResponse(data, content_type=content_type)


def site_background_image(request):
    """Отображение фоновой картинки сайта из БД."""
    settings_obj = SiteSettings.get()
    if not settings_obj.has_image:
        return HttpResponse(status=404)

    content_type = 'image/jpeg'  # по умолчанию
    try:
        data = bytes(settings_obj.background_image)
        if data[:4] == b'\x89PNG':
            content_type = 'image/png'
        elif data[:6] in (b'GIF87a', b'GIF89a'):
            content_type = 'image/gif'
    except (TypeError, ValueError):
        return HttpResponse(status=404)

    return HttpResponse(data, content_type=content_type)


def user_login(request):
    """Страница входа в аккаунт."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Вы вошли как {user.username}')
            next_url = request.GET.get('next')
            return redirect(next_url) if next_url else redirect('main:product_list')
    else:
        form = AuthenticationForm(request)

    return render(request, 'main/login.html', {'form': form})


def user_register(request):
    """Страница регистрации нового пользователя."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f'Аккаунт создан! Добро пожаловать, {user.username}',
            )
            return redirect('main:product_list')
    else:
        form = UserCreationForm()

    return render(request, 'main/register.html', {'form': form})


def user_logout(request):
    """Выход из аккаунта."""
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта')
    return redirect('main:product_list')
