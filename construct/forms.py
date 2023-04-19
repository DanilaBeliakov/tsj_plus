from django import forms
import datetime

NOTIFICATION_TIME = """
      Уведомление о проведении общего собрания членов товарищества собственников жилья направляется в письменной форме лицом, по инициативе которого созывается общее собрание, и вручается каждому члену товарищества под расписку или посредством почтового отправления (заказным письмом) либо иным способом, предусмотренным решением общего собрания членов товарищества или уставом товарищества. Уведомление направляется не позднее чем за 10 дней до даты проведения общего собрания. (ст. 146 ЖК РФ)

Обратите внимание! 
При проведении общего собрания собственников с использованием системы администратору общего собрания должно быть передано отвечающее установленным требованиям сообщение о проведении соответствующего собрания не позднее чем за 14 дней до даты начала проведения общего собрания (ст. 47.1 ЖК РФ).
"""

VOTING_TIME = """
Продолжительность голосования по вопросам повестки дня общего собрания собственников помещений в многоквартирном доме с использованием системы должна составлять не менее чем 7 дней и не более чем 60 дней с даты и времени начала проведения такого голосования (п.8 ст. 47.1 ЖК РФ).

Голосование по вопросам повестки дня общего собрания собственников помещений в многоквартирном доме с использованием системы проводится без перерыва с даты и времени его начала и до даты и времени его окончания (п.9 ст. 47.1 ЖК РФ).

"""


def get_minimum_date(delta):
    now = datetime.datetime.now().date()  # текущая дата
    u = datetime.datetime.strptime(str(now), "%Y-%m-%d")
    d = datetime.timedelta(days=delta)
    return (u + d).date()


def get_maximum_date(delta):
    now = datetime.datetime.now().date()  # текущая дата
    u = datetime.datetime.strptime(str(now), "%Y-%m-%d")
    d = datetime.timedelta(days=delta)
    return (u + d).date()


class NotificationForm(forms.Form):
    name_of_place = forms.CharField(required=False, label='Место встречи (например, номер подъезда)',
                                    widget=forms.TextInput())
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

    date_of_start = forms.DateTimeField(label='Дата начала собрания/онлайн голосования:', widget=forms.DateInput(
        attrs={'title': NOTIFICATION_TIME, 'type': 'date', 'value': '2023-05-05', 'min': get_minimum_date(14), 'onchange': "setMinDate();"}))
    time_of_start = forms.DateTimeField(required=False, label='Время начала собрания:',
                                        widget=forms.TimeInput(format='%H:%M',
                                                               attrs={'type': 'time', 'value': '12:00'}))
    date_of_end = forms.DateTimeField(required=False, label='Дата окончания заочного голосования:',
                                      widget=forms.DateInput(attrs={'type': 'date',
                                                                    'min': get_minimum_date(21),
                                                                    'title': VOTING_TIME,
                                                                    'onchange': 'setCountingDate();',
                                                                    'value': "2023-05-14",
                                                                    }))
    time_of_end = forms.DateTimeField(required=False, label='Время окончания заочного голосования:',
                                      widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'value': '18:00'}))

    date_of_counting = forms.DateTimeField(label='Дата подведения итогов:',
                                           widget=forms.DateInput(attrs={'type': 'date', 'value': '2023-05-15'}))
    time_of_counting = forms.DateTimeField(label='Время подсчета голосов:',
                                           widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'value': '20:00'}))
    place_of_counting = forms.CharField(label='Место подсчета голосов:', widget=forms.TextInput())
    questions = forms.CharField(label='Вопросы, выносимые на собрание ТСЖ:', widget=forms.TextInput())

    invited_people = forms.CharField(required=False,
                                     label='Введите имена приглашенных на собрание лиц не из числа собственников (необязательно):',
                                     widget=forms.TextInput())
    CHOICES = [
        ('6', 'Собственником'),
        ('7', 'Представлителем'),
    ]
    type_of_initiator = forms.ChoiceField(label='Кем является инициатор собрания:',
                                          widget=forms.RadioSelect(),
                                          choices=CHOICES,
                                          )
    representative_name = forms.CharField(required=False, label='ФИО представителя:', widget=forms.TextInput())
    attorney = forms.CharField(required=False, label='Номер доверенности:', widget=forms.TextInput())




