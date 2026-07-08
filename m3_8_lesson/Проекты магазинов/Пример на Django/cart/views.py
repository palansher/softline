"""Представления корзины — добавление, удаление, просмотр."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from main.models import Product

from .cart import Cart
from .forms import CartAddProductForm


@login_required
@require_POST
def cart_add(request, product_id):
    """Добавить товар в корзину."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override'],
        )
    return redirect('cart:cart_detail')


@login_required
@require_POST
def cart_remove(request, product_id):
    """Удалить товар из корзины."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    """Страница просмотра содержимого корзины."""
    cart = Cart(request)
    for item in cart:
        initial = {'quantity': item['quantity'], 'override': True}
        item['update_quantity_form'] = CartAddProductForm(initial=initial)
    return render(request, 'cart/detail.html', {'cart': cart})
