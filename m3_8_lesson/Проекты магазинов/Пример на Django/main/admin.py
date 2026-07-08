"""Админ-панель для категорий, товаров и настроек сайта."""

import base64

from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, SiteSettings


class SiteSettingsForm(forms.ModelForm):
    """Форма настроек сайта с загрузкой фона через файл."""

    background_upload = forms.FileField(
        label='Фоновое изображение',
        help_text=(
            'Загрузите картинку для фона сайта. '
            'Рекомендуемый размер: 1920×1080 px, форматы JPG/PNG.'
        ),
        required=False,
        widget=forms.ClearableFileInput(
            attrs={'style': 'width: 100%;'},
        ),
    )

    class Meta:
        model = SiteSettings
        # Все поля модели (кроме background_image — его заменяет upload-поле)
        exclude = ('background_image',)



class ProductImageDBForm(forms.ModelForm):
    """Форма товара с загрузкой изображения прямо в БД."""

    # Поле для загрузки файла, сохраняется в image_data в БД
    image_db_upload = forms.FileField(
        label='Загрузить изображение в БД',
        help_text=(
            'Выберите файл он будет сохранён прямо в базе данных '
            'и заменит текущее изображение.'
        ),
        required=False,
        widget=forms.ClearableFileInput(attrs={'style': 'width: 100%;'}),
    )

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('image_data',)  


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Административная панель управления категориями."""

    list_display = ['icon_preview', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

    @admin.display(description='Иконка')
    def icon_preview(self, obj):
        """Иконка категории в списке админки."""
        if obj.icon:
            style = (
                'width:80px;height:80px;object-fit:contain;'
                'border-radius:10px;background:#2a2e3b;'
            )
            return format_html(
                '<img src="{}" style="{}" />', obj.icon.url, style,
            )
        return '—'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Административная панель управления товарами."""

    form = ProductImageDBForm

    list_display = [
        'name', 'price', 'stock_quantity',
        'stock_status', 'available', 'category',
    ]
    list_filter = ['available', 'category']
    list_editable = ['price', 'stock_quantity']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['image_db_preview', 'has_image_in_db']

    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'name', 'slug', 'description', 'price'),
        }),
        ('Склад', {
            'fields': ('stock_quantity', 'available'),
            'classes': ('collapse',),
        }),
        ('Изображение (файл на диске)', {
            'fields': ('image',),
            'classes': ('collapse',),
        }),
        ('Изображение (в БД)', {
            'fields': ('image_db_upload', 'has_image_in_db', 'image_db_preview'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Остаток', ordering='stock_quantity')
    def stock_status(self, obj):
        """Цветной индикатор остатка на складе."""
        if obj.stock_quantity == 0:
            return '<span style="color:#ff6b6b;font-weight:700;">Нет на складе</span>'
        if obj.stock_quantity <= 5:
            color = '#fbbf24'
            text = f'{obj.stock_quantity} — мало!'
            return f'<span style="color:{color};font-weight:700;">{text}</span>'
        color = '#34d399'
        qty = obj.stock_quantity
        return f'<span style="color:{color};font-weight:600;">{qty}</span>'

    @admin.display(description='Есть в БД')
    def has_image_in_db(self, obj):
        """Показать есть ли изображение в БД."""
        if obj.image_data:
            size_kb = len(bytes(obj.image_data)) / 1024
            return format_html(
                '<span style="color:#34d399;font-weight:600;">✓ Да '
                '({:.1f} КБ)</span>', size_kb,
            )
        return '<span style="color:#6b7280;">✕ Нет</span>'

    @admin.display(description='Превью (из БД)')
    def image_db_preview(self, obj):
        """Предпросмотр изображения, хранящегося в БД."""
        if not obj.image_data:
            return 'Нет изображения в БД'

        b64 = base64.b64encode(obj.image_data[:200000]).decode('ascii')
        style = 'max-width:300px;border-radius:10px;'
        return format_html(
            '<img src="data:image/jpeg;base64,{}" style="{}" />', b64, style,
        )

    def save_model(self, request, obj, form, change):
        """Сохраняет товар и обработавает загрузку изображения в БД."""
        uploaded = form.cleaned_data.get('image_db_upload')
        if uploaded:
            obj.image_data = uploaded.read()

        super().save_model(request, obj, form, change)

        # Автоотключение при нулевом остатке
        if obj.stock_quantity <= 0:
            obj.available = False
            obj.save(update_fields=['available'])



@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Управление глобальными настройками магазина.Ы"""

    form = SiteSettingsForm
    list_display = ['id', 'bg_preview', 'background_size',
                    'background_position', 'background_attach',
                    'overlay_opacity']
    fieldsets = (
        ('Фон сайта', {
            'fields': ('background_upload', 'bg_preview'),
        }),
        ('Масштаб и позиция', {
            'fields': ('background_size', 'background_position',
                       'background_attach'),
        }),
        ('Затемнение', {
            'fields': ('overlay_opacity',),
        }),
    )
    readonly_fields = ['bg_preview']

   
    def has_add_permission(self, request):
        """Скрыть кнопку «Добавить»"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Запрет удаления единственной записи настроек."""
        return False

   
    def bg_preview(self, obj):
        """Предпросмотр фонового изображения в админке."""
        if obj.background_image:
            data = bytes(obj.background_image[:500000])
            b64 = base64.b64encode(data).decode('ascii')
            style = (
                'width:100%;max-height:300px;object-fit:cover;'
                'border-radius:8px;margin-top:10px;'
            )
            return format_html(
                '<div style="{}"><img src="data:image/jpeg;base64,{}" '
                'style="{}"/></div>', style, b64, style,
            )
        return '<span style="color:#6b7280;">Фон не загружен</span>'

    def save_model(self, request, obj, form, change):
        """Обработка загрузки файла фона в БД."""
        uploaded = form.cleaned_data.get('background_upload')
        if uploaded:
            obj.background_image = uploaded.read()

        super().save_model(request, obj, form, change)
