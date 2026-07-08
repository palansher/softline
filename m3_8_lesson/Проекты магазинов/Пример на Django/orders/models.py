"""Модели заказов и позиций заказа."""

from django.conf import settings
from django.db import models

from main.models import Product


class Order(models.Model):
    """Заказ покупателя. Привязан к пользователю через FK."""

    STATUS_CHOICES = [
        ('pending', 'Ожидает обработки'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    # Словарь для массовых действий в админке
    STATUS_MAP = dict(STATUS_CHOICES)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='orders',
        null=True, blank=True,
        verbose_name="Пользователь",
    )
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(
        max_length=250, verbose_name="Адрес доставки",
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлён")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending',
        verbose_name="Статус",
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        user_str = self.user.username if self.user else 'Гость'
        return f'Заказ № {self.id} — {user_str}'

    @property
    def total_price(self):
        """Общая стоимость всех позиций заказа."""
        return sum(item.line_price for item in self.items.all())


class OrderItem(models.Model):
    """Отдельная позиция в заказе."""

    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product, related_name='order_items',
        on_delete=models.CASCADE, verbose_name="Товар",
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена за шт.",
    )
    quantity = models.PositiveIntegerField(
        default=1, verbose_name="Количество",
    )

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'

    def __str__(self):
        return (
            f'{self.product.name} (×{self.quantity}) в заказе № {self.order.id}'
        )

    @property
    def line_price(self):
        """Стоимость данной позиции: цена × количество."""
        return self.price * self.quantity
