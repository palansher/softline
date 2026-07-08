"""Представления заказов — создание, история, детали, отмена."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart

from .forms import OrderCreateForm
from .models import Order, OrderItem


@login_required
@transaction.atomic
def order_create(request):
    """Оформление нового заказа из корзины.

    Весь процесс выполняется внутри одной транзакции: создание заказа,
    списание товаров со склада. При любой
    ошибке транзакция откатывается и заказ не появляется.
    """
    cart = Cart(request)
    if not cart.cart:
        messages.warning(request, 'Корзина пуста!')
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # --- первичная проверка наличия на складе -------------
            insufficient = []
            for item in cart:
                product = item['product']
                if not product.has_stock(item['quantity']):
                    insufficient.append(product.name)

            if insufficient:
                messages.error(
                    request,
                    f'Недостаточно на складе: {", ".join(insufficient)}. '
                    'Удалите их из корзины или уменьшите количество.',
                )
                return redirect('cart:cart_detail')

            # --- создание заказа внутри транзакции -----------------
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # --- списание со склада ---------------------
            failed_products = []
            for item in cart:
                product = item['product']
                success = product.reduce_stock_atomic(item['quantity'])
                if not success:
                    failed_products.append(product.name)

            if failed_products:
                messages.error(
                    request,
                    f'Не удалось забронировать: {", ".join(failed_products)}. '
                    'Кто-то уже купил последние экземпляры.',
                )
                # --- Откат транзакции — заказ удалится автоматически -------------------------
                order.delete()
                return redirect('cart:cart_detail')

            # --- сохранение позиций заказа -------------------------
            for item in cart:
                product = item['product']
                OrderItem.objects.create(
                    order=order, product=product,
                    price=item['price'], quantity=item['quantity'],
                )

            cart.clear()
            messages.success(
                request, f'Заказ #{order.id} успешно оформлен!',
            )
            return redirect('orders:order_history')
    else:
        form = OrderCreateForm()

    return render(request, 'orders/create.html', {'cart': cart, 'form': form})


@login_required
@transaction.atomic
def order_cancel(request, order_id):
    """Отмена заказа — возврат товаров на склад."""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status in ('delivered', 'cancelled'):
        messages.error(
            request, f'Заказ уже {order.get_status_display()}.',
        )
        return redirect('orders:order_detail', order_id=order.id)

    for item in order.items.all():
        item.product.restore_stock(item.quantity)

    order.status = 'cancelled'
    order.save(update_fields=['status'])
    messages.success(
        request,
        f'Заказ #{order.id} отменён. Товары возвращены на склад.',
    )
    return redirect('orders:order_detail', order_id=order.id)


@login_required
def order_history(request):
    """Список заказов текущего пользователя."""
    orders = Order.objects.filter(
        user=request.user,
    ).prefetch_related('items__product')
    return render(request, 'orders/history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """Детальная страница одного заказа."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})
