"""
URL configuration for lesson34 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from my_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index),
    path("pass_data", views.pass_data),
    path("pass_data_v2/<str:name>/<int:age>/", views.pass_data_v2),
    path('calc/<int:a>/<int:b>/<str:sign>', views.calc),
    path('test_template/',views.test_template),
    path('form/',views.form),
    path('get_data_from_form/',views.get_data_from_form), # type: ignore
    path('demo_ajax/',views.demo_ajax),

    #Новые запросы
    
    # http://127.0.0.1:8000/parse_data/
    path('parse_data/', views.demo_parse_data_in_template),
    # http://127.0.0.1:8000/catalog
    path('catalog/', views.catalog),
    
    # http://127.0.0.1:8000/card
    path('card/', views.card),
    
    # http://127.0.0.1:8000/add_car
    path('add_car/', views.add_car),
    
    # http://127.0.0.1:8000/show_cars
    path('show_cars/', views.show_cars),
    
    # http://127.0.0.1:8000/get_cars
    path('get_cars/', views.get_cars),
    
    # http://127.0.0.1:8000/simple_catalog
    path('simple_catalog/', views.simple_catalog),
    
    # http://127.0.0.1:8000/create_query
    path('create_query/', views.create_query),
    
    # http://127.0.0.1:8000/update
    path('update/', views.demo_update),
    
    # http://127.0.0.1:8000/demo_delete
    path('demo_delete/', views.demo_delete),
    
    # http://127.0.0.1:8000/get_car/?id=1
    path('get_car/', views.get_car),
    
    # http://127.0.0.1:8000/test_cursor
    path('test_cursor/', views.test_cursor)

]
