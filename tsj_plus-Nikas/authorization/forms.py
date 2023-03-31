from django import forms
from .models import users
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(forms.Form):
    full_name = forms.CharField(label='Имя:', widget=forms.TextInput(attrs={"class":"myfield", 'style':'width: 400px; height: 40px;'}))
    # username = forms.CharField(label='Логин:', widget=forms.TextInput(attrs={"class":"myfield"}))
    email = forms.CharField(label='Почта:', widget=forms.TextInput(attrs={"class":"myfield", 'style':'width: 400px; height: 40px;'}))
    address = forms.CharField(label='Полный адрес дома:', widget=forms.TextInput(attrs={"class":"myfield", 'style':'width: 400px; height: 40px;'})) # help_text='Город, улица, дом'
    flat_number = forms.CharField(label='Номер квартиры:', widget=forms.TextInput(attrs={"class":"myfield", 'style':'width: 400px; height: 40px;'})) # help_text='Город, улица, дом'
    password_first = forms.CharField(label='Пароль:', widget=forms.PasswordInput(attrs={"class":"myfield", 'style':'width: 400px; height: 40px;'}))
    password_second = forms.CharField(label='Подтверждение пароля:', widget=forms.PasswordInput(attrs={"class":"myfield", 'style':'width: 400px; height: 40px;'}))
    class Meta:
        model = users
        fields = ("full_name", "email", 'flat_number', 'address', 'password_first', 'password_second')

class AuthForm(forms.Form):
    email = forms.CharField(label='Почта:', widget=forms.TextInput(attrs={"class": "myfield", 'style':'width: 400px; height: 40px;'}))
    password = forms.CharField(label='Пароль:', widget=forms.PasswordInput(attrs={"class":"myfield", 'style':'width: 400px; height: 40px;'}))