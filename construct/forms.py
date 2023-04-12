from django import forms
import datetime


def get_minimum_date():
    now = datetime.datetime.now().date() # текущая дата
    u = datetime.datetime.strptime(str(now), "%Y-%m-%d")
    d = datetime.timedelta(days=10)
    return (u+d).date()


class NotificationForm(forms.Form):
    name_of_place = forms.CharField(required=False, label='Место встречи (например, номер подъезда)', widget=forms.TextInput())
    CHOICES = [
        ('1', 'Очное'),
        ('2', 'Заочное'),
        ('3', 'Очно-заочное'),
    ]
    type_of_meeting = forms.ChoiceField(label='Тип собрания и голосования:',
        widget=forms.RadioSelect,
        choices=CHOICES,
    )
    CHOICES = [
        ('4', 'Внеочередное'),
        ('5', 'Очередное'),
    ]
    type_of_plans = forms.ChoiceField(label='Тип собрания:',
                                        widget=forms.RadioSelect,
                                        choices=CHOICES,
                                        )


    date_of_start = forms.DateTimeField(label='Дата начала собрания/онлайн голосования:', widget=forms.DateInput(attrs={'type': 'date', 'value':get_minimum_date(),'min': get_minimum_date()}))
    time_of_start = forms.DateTimeField(required=False, label='Время начала собрания:', widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'value': '12:00'}))
    date_of_end = forms.DateTimeField(required=False, label='Дата окончания заочного голосования:', widget=forms.DateInput(attrs={'type': 'date','value':get_minimum_date(),'min': get_minimum_date()}))
    time_of_end = forms.DateTimeField(required=False, label='Время окончания заочного голосования:',widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'value': '12:00'}))

    date_of_counting = forms.DateTimeField(label='Дата подсчета голосов:',
                                        widget=forms.DateInput(attrs={'type': 'date'}))
    time_of_counting = forms.DateTimeField(label='Время подсчета голосов:',
                                        widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}))
    place_of_counting = forms.CharField(label='Место подсчета голосов:', widget=forms.TextInput())
    questions = forms.CharField(label='Вопросы, выносимые на собрание ТСЖ:', widget=forms.TextInput())

    invited_people = forms.CharField(required=False, label='Введите имена приглашенных на собрание лиц не из числа собственников (необязательно):', widget=forms.TextInput())
    CHOICES = [
        ('4', 'Собственником'),
        ('5', 'Представлителем'),
    ]
    type_of_initiator = forms.ChoiceField(label='Кем является инициатор собрания:',
        widget=forms.RadioSelect(),
        choices=CHOICES,
    )
    representative_name = forms.CharField(required=False, label='ФИО представителя:', widget=forms.TextInput())
    attorney = forms.CharField(required=False, label='Номер доверенности:', widget=forms.TextInput())

    





