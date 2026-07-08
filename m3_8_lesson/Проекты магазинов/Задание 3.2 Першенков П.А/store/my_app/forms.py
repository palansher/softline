from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from .models import *


class OrdersForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['user_name', 'user_phone']
        db_table = 'orders'

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


