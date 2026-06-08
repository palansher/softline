"""
URL configuration for lesson3 project.

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
    path('get_data_from_form/',views.get_data_from_form),
    path('demo_ajax/',views.demo_ajax),

]
