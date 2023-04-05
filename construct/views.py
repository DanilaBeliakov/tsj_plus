from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.http import HttpResponse, FileResponse
from .forms import NotificationForm
import datetime
from django.utils.dateparse import parse_datetime
import sys
import os
from .models import meetings
from authorization.models import users, houses
sys.path.append(os.getcwd())
from docxtpl import DocxTemplate

def index_construct(request):
    all = meetings.all_elements(house=request.session['house_id'])
    return render(
            request,
            'index_construct.html',
            context = {'all':all},
    )


def meeting_view(request):
    meeting_id = request.GET.get('id')
    meeting = meetings.objects.get(meeting_id=meeting_id)
    return render(request, 'meeting.html', context={'meeting': meeting})


def notification_view(request):
    if request.method == 'POST':
        tsj_name = request.POST.get('tsj_name')
        name_of_place = request.POST.get('name_of_place')
        type_of_meeting = request.POST.get('type_of_meeting')
        date_of_start = request.POST.get('date_of_start')
        date_of_end = request.POST.get('date_of_end')
        questions = request.POST.get('questions').split(',')
        invited_people = request.POST.get('invited_people')

        doc = DocxTemplate("/home/d0nald/PycharmProjects/TSH_Site/tsjsite/construct/notification.docx")
        user = users.objects.get(email=request.session['email'])
        house = houses.objects.get(id=request.session['house_id'])
        meeting = meetings.objects.get(meeting_id=1)
        if type_of_meeting == 'Очное':
            face_to_face = True
            online = False
        elif type_of_meeting == 'Заочное':
            face_to_face = False
            online = True
        else:
            face_to_face = True
            online = True

        context = {'face_to_face': face_to_face,
                   'name_of_place': name_of_place,
                   'online': online,
                   'user': user,
                   'house': house,
                   'meeting': meeting,
                   'tsj_name': tsj_name,
                   'questions': questions,
                   'date_of_start': date_of_start,
                   'date_of_end': date_of_end,
                   }
        doc.render(context)
        doc.save('example.docx')


        return FileResponse(open('example.docx', 'rb'))
    else:
        form = NotificationForm()
        return render(request,
                      'notification_creation.html',
                      context={
                          'form': form,
                      })


def generate_docx(request):
    doc = DocxTemplate("/home/d0nald/PycharmProjects/TSH_Site/tsjsite/construct/notification.docx")
    user = users.objects.get(email=request.session['email'])
    house = houses.objects.get(id=request.session['house_id'])
    meeting = meetings.objects.get(meeting_id=1)
    context = {'address': 'ул. Пушкина, дом Колотушкина',
               'face_to_face': False,
               'online': True,
               'user': user,
               'house': house,
               'meeting':meeting,
               'tsj_name': 'ЖК Примерное',
               'questions': ['question1', 'question2']}
    doc.render(context)
    doc.save('example.docx')
    return HttpResponse("hi")