from django import forms
from .models import users
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(forms.Form):
    full_name = forms.CharField(label='Имя:', widget=forms.TextInput(attrs={"class":"myfield", 'style':'width: 400px; height: 40px;', 'name': 'full_name', 'pattern': "[а-яА-Я ]*$", 'title': "Только кириллица и пробелы", 'minlength':'10', 'maxlength': '100',}))
    email = forms.CharField(label='Почта:', widget=forms.TextInput(attrs={"class":"myfield", 'style':'width: 400px; height: 40px;', 'name': 'email', 'pattern': "[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$", 'title': "Пример: example@example.com"}))
    address = forms.CharField(label='Полный адрес дома:', widget=forms.TextInput(attrs={"class":"myfield", 'style':'width: 400px; height: 40px;', 'pattern': "^[а-яА-Я ,.\d\/]*$", 'title': 'Только кириллица, цифры и символы . и ,', 'minlength': '10', 'maxlength': '100'}))
    flat_number = forms.CharField(label='Номер квартиры:', widget=forms.TextInput(attrs={"class":"myfield", 'style':'width: 400px; height: 40px;', 'pattern': "^[\d]*$", 'maxlength': 10, 'minlength': '1'}))
    password_first = forms.CharField(label='Пароль:', widget=forms.PasswordInput(attrs={"class":"myfield", 'style':'width: 400px; height: 40px;', 'minlength': '8', 'maxlength': '16', 'title': 'Длина пароля от 8 до 16 символов'}))
    flat_area = forms.CharField(label='Площадь личной квартиры:', widget=forms.TextInput(attrs={"class":"myfield", 'style':'width: 400px; height: 40px;', 'pattern': "^[\d.]*$", 'title': 'Можно вводить только цифры и символ  точки'}))
    flat_share = forms.CharField(label='Доля в личной квартире:', widget=forms.TextInput(attrs={"class":"myfield", 'style':'width: 400px; height: 40px;', 'pattern': "^[\d\/]*$", 'placeholder': 'Например, 1 или 1/3'}))

    class Meta:
        model = users
        fields = ("full_name", "email", 'flat_number', 'address', 'password_first', 'flat_area', 'flat_share')


class AuthForm(forms.Form):
    email = forms.CharField(label='Почта:', widget=forms.TextInput(attrs={"class": "myfield", 'style':'width: 400px; height: 40px;'}))
    password = forms.CharField(label='Пароль:', widget=forms.PasswordInput(attrs={"class":"myfield", 'style':'width: 400px; height: 40px;'}))