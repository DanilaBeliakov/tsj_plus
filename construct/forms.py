from django import forms


class NotificationForm(forms.Form):
    tsj_name = forms.CharField(label='Название ТСЖ', widget=forms.TextInput())
    name_of_place = forms.CharField(label='Место встречи', widget=forms.TextInput())
    CHOICES = [
        ('1', 'Очное'),
        ('2', 'Заочное'),
        ('3', 'Очно-заочное'),
    ]
    type_of_meeting = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES,
    )
    date_of_start = forms.DateTimeField(label='Начало собрания', widget=forms.DateTimeInput())
    date_of_end = forms.DateTimeField(label='Конец собрания', widget=forms.DateTimeInput())
    questions = forms.CharField(label='Вопросы, выносимые на собрание ТСЖ:', widget=forms.TextInput())
    invited_people = forms.CharField(label='Введите имена приглашенных на собрание лиц не из числа собственников', widget=forms.TextInput())


