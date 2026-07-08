"""Формы корзины."""

from django import forms

# Допустимые значения количества при добавлении в корзину
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]


class CartAddProductForm(forms.Form):
    """Форма добавления товара в корзину с выбором количества."""

    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,
        label='Количество',
        widget=forms.Select(attrs={
            'class': (
                'form-select form-select-sm d-inline-block '
                'w-auto me-2'
            ),
        }),
    )
    override = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput,
    )
