"""URL-маршруты заказов."""

from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('my-orders/', views.order_history, name='order_history'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path(
        'order/<int:order_id>/cancel/',
        views.order_cancel, name='order_cancel',
    ),
]
