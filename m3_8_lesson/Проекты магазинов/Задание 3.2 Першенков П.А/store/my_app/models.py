from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Item(models.Model):
    item_id = models.IntegerField()
    title = models.CharField(max_length=30)
    price = models.IntegerField()
    info = models.TextField()
    photo = models.CharField(max_length=100)


class Cart(models.Model):
    user_id = models.IntegerField(default=0)
    item_id = models.IntegerField()
    quantity = models.IntegerField()

class Orders(models.Model):
    user_id = models.IntegerField()
    user_phone = models.CharField(max_length=15,)
    user_name = models.CharField(max_length=30, default ="user")
