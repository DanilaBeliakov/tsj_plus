from django import forms
from authorization.models import users, houses

class NewUserForm(forms.Form):
    full_name = forms.CharField(label='Имя:',
                                widget=forms.TextInput(
                                attrs={"class": "myfield",
                                       'style': 'width: 400px; height: 40px;'}))
    # username = forms.CharField(label='Логин:', widget=forms.TextInput(attrs={"class":"myfield"}))
    email = forms.CharField(label='Почта:',
                            widget=forms.TextInput(attrs={"class": "myfield", 'style': 'width: 400px; height: 40px;'}))
    flat_number = forms.CharField(label='Номер квартиры:', widget=forms.TextInput(attrs={"class": "myfield",
                                                                                         'style': 'width: 400px; height: 40px;'}))  # help_text='Город, улица, дом'
    class Meta:
        model = users
        fields = ("full_name", "email", 'flat_number')