from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser


class users(AbstractUser):
    user_id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=50)
    house_id = models.IntegerField()
    flat_number = models.IntegerField()
    is_admin = models.BooleanField(default=False)

    # objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','full_name', 'house_id', 'flat_number', 'is_admin']

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class houses(models.Model):
    address = models.CharField(max_length=200)
