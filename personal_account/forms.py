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
    flat_area = forms.CharField(label='Площадь квартиры:', widget=forms.TextInput(
                                                                                    attrs={"class": "myfield", 'style': 'width: 400px; height: 40px;'}))
    flat_share = forms.CharField(label='Доля в квартире:', widget=forms.TextInput(
                                                                                    attrs={"class": "myfield", 'style': 'width: 400px; height: 40px;'}))

    class Meta:
        model = users
        fields = ("full_name", "email", 'flat_number', 'flat_area', 'flat_share')


class ChangeForm(NewUserForm):
    password = forms.CharField(required=False, label='Новый пароль:', widget=forms.PasswordInput(attrs={"class": "myfield", 'style': 'width: 400px; height: 40px;'}))


class TsjInfoForm(forms.Form):
    tsj_name = forms.CharField(label='Название ТСЖ:', widget=forms.TextInput(attrs={"class": "myfield", 'style': 'width: 400px; height: 40px;'}))
    address = forms.CharField(label='Полный адрес дома:', widget=forms.TextInput(attrs={"class": "myfield", 'style': 'width: 400px; height: 40px;'}))
    house_area = forms.CharField(label='Жилая площадь дома: ', widget=forms.TextInput(attrs={"class": "myfield", 'style': 'width: 400px; height: 40px;'}))
    inn = forms.CharField(required=False, label='ИНН ТСЖ (если есть):', widget=forms.TextInput(attrs={"class": "myfield", 'style': 'width: 400px; height: 40px;'}))
    ogrn = forms.CharField(required=False, label='ОГРН ТСЖ (если есть):', widget=forms.TextInput(attrs={"class": "myfield", 'style': 'width: 400px; height: 40px;'}))
