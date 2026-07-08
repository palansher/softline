"""URL-маршруты главного приложения."""

from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('image/<int:product_id>/', views.product_image_db, name='product_image_db'),
    path('bg-image/', views.site_background_image, name='site_background_image'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]
