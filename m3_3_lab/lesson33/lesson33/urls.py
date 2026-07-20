"""
URL configuration for lesson33 project.

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

"""
Пайланс (Pylance) видит тип вашей функции как HttpResponse | str | None. Он сверяет это со встроенными типами Django и понимает, что такая функция не может быть валидным view. Из-за этого он путается и пытается сопоставить её с другими вариантами (overloads) функции path, выдавая странную ошибку про кортежи (tuple).

Как исправить
Вам нужно сделать так, чтобы при любом раскладе функция возвращала HttpResponse.
"""

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index),  # Название маршрута (name) можно не писать.
    path("pass_data", views.pass_data),
    # http://127.0.0.1:8000/pass_data_v2/Ivan/25
    path("pass_data_v2/<str:name>/<int:age>/", views.pass_data_v2),
    # http://127.0.0.1:8000/calc/2/3/+, http://127.0.0.1:8000/calc/2/3/%2b
    path("calc/<int:a>/<int:b>/<str:sign>", views.calc),
    # http://127.0.0.1:8000/test_template/
    path("test_template/", views.test_template),
    # http://127.0.0.1:8000/form/
    path("form/", views.form),
    # http://127.0.0.1:8000/form/
    path("get_data_from_form/", views.get_data_from_form),
    # http://127.0.0.1:8000/demo_ajax/
    path("demo_ajax/", views.demo_ajax),
]
