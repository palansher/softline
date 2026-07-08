"""Админ-панель заказов и позиций."""

from django.contrib import admin
from django.utils.html import format_html

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Встроенный список позиций внутри страницы заказа."""

    model = OrderItem
    fields = ['product', 'price', 'quantity', 'line_price']
    readonly_fields = ['line_price']
    extra = 0

    @admin.display(description='Сумма')
    def line_price(self, obj):
        """Подсчитанная сумма по позиции."""
        return f'{obj.line_price} ₽' if obj.id else '—'


def _mark_status(modeladmin, request, queryset, new_status):
    """ установка *new_status* для выбранных заказов."""
    count = queryset.update(status=new_status)
    label = Order.STATUS_MAP[new_status]
    modeladmin.message_user(
        request, f'{count} заказ(ов) помечен как «{label}».',
    )


def mark_pending(modeladmin, request, queryset):
    _mark_status(modeladmin, request, queryset, 'pending')
mark_pending.short_description = '❓ Пометить как ожидающие'


def mark_processing(modeladmin, request, queryset):
    _mark_status(modeladmin, request, queryset, 'processing')
mark_processing.short_description = '\U0001f527 Пометить в обработке'


def mark_shipped(modeladmin, request, queryset):
    _mark_status(modeladmin, request, queryset, 'shipped')
mark_shipped.short_description = '\U0001f69a Пометить как отправленные'


def mark_delivered(modeladmin, request, queryset):
    _mark_status(modeladmin, request, queryset, 'delivered')
mark_delivered.short_description = '✅ Пометить как доставленные'


def mark_cancelled(modeladmin, request, queryset):
    _mark_status(modeladmin, request, queryset, 'cancelled')
mark_cancelled.short_description = '❌ Отменить выбранные заказы'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Административная панель управления заказами."""

    list_display = [
        'id', 'user_short', 'status_badge', 'status',
        'total_badge', 'created',
    ]
    list_filter = ['status', 'created', 'user__username']
    search_fields = [
        'id', 'first_name', 'last_name', 'email', 'phone', 'user__username',
    ]
    readonly_fields = ['id', 'created', 'updated', 'total_display']
    list_editable = ['status']  # редактирование статуса прямо в списке
    ordering = ['-created']

    # Массовые действия над выбранными заказами
    actions = [
        mark_pending,
        mark_processing,
        mark_shipped,
        mark_delivered,
        mark_cancelled,
    ]

    fieldsets = (
        ('Заказ', {
            'fields': ('id', 'user', 'status', 'created', 'updated'),
        }),
        ('Данные покупателя', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'address'),
        }),
        ('Итого', {'fields': ('total_display',)}),
    )
    inlines = [OrderItemInline]

    @admin.display(description='Покупатель', ordering='user__username')
    def user_short(self, obj):
        """Краткое имя пользователя для списка заказов."""
        return f'{obj.user.username} (#{obj.user.id})'

    @admin.display(description='Статус')
    def status_badge(self, obj):
        """Цветной бейдж статуса заказа."""
        color_map = {
            'pending': '#f59e0b',
            'processing': '#3b82f6',
            'shipped': '#8b5cf6',
            'delivered': '#10b981',
            'cancelled': '#ef4444',
        }
        color = color_map.get(obj.status, '#6b7280')
        return (
            f'<span style="color:{color};font-weight:700;">'
            f'●</span> {obj.get_status_display()}'
        )

    @admin.display(description='Итого', ordering='items')
    def total_badge(self, obj):
        """Суммарная стоимость заказа в списке."""
        return f'{obj.total_price} ₽'

    @admin.display(description='Итоговая сумма')
    def total_display(self, obj):
        """Отображение итоговой суммы на странице заказа."""
        return f'{obj.total_price} ₽'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Административная панель отдельных позиций заказов."""

    list_display = ['id', 'order', 'product', 'price', 'quantity', 'line_price']
    list_filter = ['order__status']

    @admin.display(description='Сумма')
    def line_price(self, obj):
        """Подсчитанная сумма по позиции."""
        return f'{obj.line_price} ₽'
