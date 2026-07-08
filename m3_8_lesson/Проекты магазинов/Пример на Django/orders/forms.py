"""Формы заказов."""

from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    """Форма оформления заказа — данные покупателя."""

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']
