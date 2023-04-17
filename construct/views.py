from django.shortcuts import render

# Create your views here.

from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, FileResponse
import datetime
from django.utils.dateparse import parse_datetime
import sys
import os
from .models import meetings, temp_elections, notification,statement, protocol
sys.path.append(os.getcwd())
from voting.models import elections
from authorization.models import houses, users
from news.models import news
from docxtpl import DocxTemplate
from .forms import NotificationForm
from .forms import NotificationForm
from django.core.files.base import ContentFile
from io import BytesIO
import uuid
from django.conf import settings
base_path = os.path.join(settings.BASE_DIR, 'path', 'to', 'file')
from .forms import get_minimum_date, get_maximum_date


def index_construct(request):
    all = meetings.all_elements(house=request.session['house_id'])
    now_user = users.objects.get(email=request.session['email'])

    is_index_meeting = True
    return render(
            request,
            'index_construct.html',
            context = {'all':all, 'now_user': now_user, 'is_index_meeting': is_index_meeting},
    )

def meeting_view(request):
    if request.method == 'POST':
        meeting_id = request.GET.get('id')
        meeting = meetings.objects.get(meeting_id=meeting_id)
        if request.POST.get('status') == "START" and meeting.stage == 3:
            now_elections = elections.objects.filter(meeting = meeting)
            for elem in now_elections:
                elem.is_working = 1
                elem.save()
                meeting.stage = 4
                meeting.save()
        elif request.POST.get('status') == "STOP" and meeting.stage == 4:
            now_elections = elections.objects.filter(meeting = meeting)
            for elem in now_elections:
                elem.is_working = 2
                elem.save()
                meeting.stage = 5
                meeting.save()

    meeting_id = request.GET.get('id')
    meeting = meetings.objects.get(meeting_id=meeting_id)
    request.session['meeting_id'] = meeting_id
    now_elections = elections.objects.filter(meeting=meeting)
    quorum = 1
    for elect in now_elections:
        if elect.is_quorum == 0:
            quorum = 0
    now_user = users.objects.get(email=request.session['email'])
    if now_user.user_id == meeting.initiator_id:
        is_initiator = True
    else:
        is_initiator = False
    return render(request, 'meeting.html',
                  context={'meeting': meeting, 'quorum': quorum, 'now_user': now_user, "is_initiator": is_initiator})


def add_meeting(request, voting_mas = []):
    if request.method == "POST":
        if request.POST.get('status') == "NO":
            new = request.POST.get('new_election')
            if not(temp_elections.objects.filter(question = new, house_id = request.session['house_id']).exists()):
                now_temp = temp_elections.objects.filter(house_id = request.session['house_id'])
                num_in_meeting_max = 0
                for elem in now_temp:
                    num_in_meeting_max = max(elem.num_in_meeting, num_in_meeting_max)
                new_elect = temp_elections()
                new_elect.num_in_meeting = num_in_meeting_max + 1
                new_elect.question = new
                new_elect.house_id = request.session['house_id']

                new_elect.save()
                new_elections = temp_elections.objects.filter(house_id = request.session['house_id'])
            else:
                new_elections = temp_elections.objects.filter(house_id = request.session['house_id'])
        else:
            add_elections = temp_elections.objects.filter(house_id = request.session['house_id'])
            new_meeting = meetings()
            now_user = users.objects.get(email=request.session['email'])
            now_house = houses.objects.get(id = request.session['house_id'])
            new_meeting.stage = 1
            new_meeting.title = request.POST.get('title')
            new_meeting.house_id = now_house.id
            new_meeting.date = "2001-01-01"
            new_meeting.initiator_id = now_user.user_id
            new_meeting.save()
            for elem in add_elections:
                elect = elections()
                elect.question = elem.question
                elect.num_in_meeting = elem.num_in_meeting
                elect.voited_for_area = 0
                elect.voited_against_area = 0
                elect.voited_for_part = 0
                elect.voited_against_part = 0
                elect.house = now_house
                elect.meeting = new_meeting
                elect.is_working = 0
                elect.save()
            link = "/construct/meeting/?id=" + str(new_meeting.meeting_id)
            add_new = news()
            add_new.news_text = "Собрание под названием " + new_meeting.title + " создано. Вы можете перейти по ссылке на страницу этого собрания, нажав на новость."
            add_new.house_id = now_house.id
            add_new.meeting = new_meeting
            add_new.need_link = True
            add_new.save()
            return redirect(link)
    else:
        to_del = temp_elections.objects.filter(house_id = request.session['house_id'])
        for elem in to_del:
            elem.delete()
        new_elections = temp_elections.objects.filter(house_id = request.session['house_id'])
    return render(request, 'add_meeting.html', context={'new_elections' : new_elections})


def notification_view(request):
    if request.method == 'POST':
        name_of_place = request.POST.get('name_of_place')  # место встречи для очного собрания
        type_of_meeting = request.POST.get('type_of_meeting')  # тип собрания
        planned = request.POST.get('type_of_plans')  # тип собрания
        date_of_start = request.POST.get('date_of_start')
        time_of_start = request.POST.get('time_of_start')
        date_of_end = request.POST.get('date_of_end')
        time_of_end = request.POST.get('time_of_end')
        invited_people = request.POST.get('invited_people')
        place_of_results = request.POST.get('place_of_results')
        date_of_counting = request.POST.get('date_of_counting')
        time_of_counting = request.POST.get('time_of_counting')
        place_of_counting = request.POST.get('place_of_counting')
        type_of_initiator = request.POST.get('type_of_initiator')
        representative_name = request.POST.get('representative_name')
        attorney = request.POST.get('attorney')
        if type_of_initiator == '7':
            is_representative = True
        else:
            is_representative = False

        doc = DocxTemplate("notification.docx")
        user = users.objects.get(email=request.session['email'])
        house = houses.objects.get(id=request.session['house_id'])
        meeting = meetings.objects.get(meeting_id=request.session['meeting_id'])
        meeting.stage = 2
        meeting.save()

        now_elections = elections.choose_elements(house_id=request.session['house_id'], meeting_id=request.session['meeting_id'])
        del request.session['meeting_id']
        voting = ""
        if type_of_meeting == "1":
            face_to_face = True
            online = False
            voting = 'очное'
            voting_text = 'очного'
        elif type_of_meeting == "2":
            face_to_face = False
            online = True
            voting = 'заочное'
            voting_text = 'заочного'
        else:
            face_to_face = True
            online = True
            voting = 'очно-заочное'
            voting_text = 'очно-заочного'
        if planned == "4":
            planned = 'очередное'
        else:
            planned = 'внеочередное'
        questions = []
        for val in now_elections:
            questions.append(val.question)
            print(val.question)
        context = {'face_to_face': face_to_face,
                   'name_of_place': name_of_place,
                   'online': online,
                   'user': user,
                   'house': house,
                   'meeting': meeting,
                   'questions': questions,
                   'date_of_start': date_of_start,
                   'time_of_start': time_of_start,
                   'date_of_end': date_of_end,
                   'time_of_end': time_of_end,
                   'date_of_initiation': datetime.datetime.now().strftime("%d-%m-%Y"),
                   'is_representative': is_representative,
                   'representative_name': representative_name,
                   'attorney': attorney,
                   'place_of_counting': place_of_counting,
                   'invited_people': invited_people,
                   'place_of_results': place_of_results,
                   'date_of_counting': date_of_counting,
                   'time_of_counting': time_of_counting,
                   'type_of_plans': planned,
                   'voting_text' : voting_text,
                   }
        doc.render(context)
        now = datetime.datetime.now()
        filename = f"{now.strftime('%Y-%m-%d_%H-%M-%S')}_{uuid.uuid4().hex}.docx"
        buffer = BytesIO()
        doc.save(buffer)
        docx_file = ContentFile(buffer.getvalue())
        instance = notification.objects.create(type_of_voting=voting, type_of_plans=planned,
                                               place_of_meeting=name_of_place, date_of_start=date_of_start,
                                               time_of_start=time_of_start, date_of_end=date_of_end,
                                               time_of_end=time_of_end)
        instance.notification_file.save(filename, docx_file, save=True)
        meeting.notification = instance
        meeting.save()


        link = "/construct/meeting/?id=" + str(meeting.meeting_id)
        return redirect(link)
    else:
        form = NotificationForm()
        return render(request,
                      'notification_creation.html',
                      context={
                          'form': form,
                      })
    
    
def add_statement(request):
    if request.method == 'POST':
        meeting = meetings.objects.get(meeting_id = request.session['meeting_id'])
        now_user = users.objects.get(email=request.session['email'])
        now_house = houses.objects.get(id=request.session['house_id'])
        now_elections = elections.choose_elements(house_id=now_house.id, meeting_id = meeting.meeting_id)
        tsj_name = now_house.tsj_name
        type_of_meeting = meeting.notification.type_of_voting
        if type_of_meeting == 'Очное':
            type_of_meeting = "очного"
        elif type_of_meeting == 'Заочное':
            type_of_meeting = "зачного"
        else:
            type_of_meeting = "очно-заочного"

        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        send_date = request.POST.get("send_date")
        date_of_start = meeting.notification.date_of_start
        publication_date = request.POST.get("publication_date")

        for elect in now_elections:
            ses = str(elect.election_id)
            elect.solution = request.POST.get(ses)
            elect.save()
        now_elections = elections.choose_elements(house_id = request.session['house_id'],meeting_id = meeting.meeting_id)
        context = {
                    'publication_date': publication_date,
                    'start_time' : start_time,
                    'end_time' : end_time,
                    'send_date' : send_date,
                    'date_of_start' : date_of_start,
                    'now_elections' : now_elections,
                    'type_of_meeting' : type_of_meeting,
                    'now_user': now_user,
                    'now_house': now_house,
                    'meeting': meeting,
                    'tsj_name': tsj_name,
                   }
        
        doc = DocxTemplate("statement.docx")
        doc.render(context)

        now = datetime.datetime.now()
        filename = f"{now.strftime('%Y-%m-%d_%H-%M-%S')}_{uuid.uuid4().hex}.docx"
        buffer = BytesIO()
        doc.save(buffer)
        docx_file = ContentFile(buffer.getvalue())

        now_statement = statement()
        now_statement.statement_file.save(filename, docx_file, save=True)

        meeting.stage = 3
        meeting.statement = now_statement
        meeting.save()
 
        link = "/construct/meeting/?id=" + str(meeting.meeting_id)
        return redirect(link)
    else:
        min_blanks = str(get_minimum_date(21))
        min_pub = str(get_minimum_date(21))
        max_pub = str(get_maximum_date(84))
        meeting = meetings.objects.get(meeting_id=request.session['meeting_id'])
        now_elections = elections.choose_elements(house_id=request.session['house_id'], meeting_id=meeting.meeting_id)
        # get minimum_date
        return render(request,
                      'add_statement.html',
                      context={'now_elections': now_elections, 'min_blanks': min_blanks, 'min_pub': min_pub,
                               'max_pub': max_pub}
                      )

def add_protocol(request):
    if request.method == 'POST':
        meeting = meetings.objects.get(meeting_id=request.session['meeting_id'])
        notify = notification.objects.get(notification_id=meeting.notification_id)
        type_of_meeting = notify.type_of_voting
        if type_of_meeting == 'Очное':
            type_of_meeting = "очного"
        elif type_of_meeting == 'Заочное':
            type_of_meeting = "зачного"
        else:
            type_of_meeting = "очно-заочного"

        initiator_name = request.POST.get('initiator_name')
        chairman_name = request.POST.get('chairman_name')
        secretary_name = request.POST.get('secretary_name')
        counters_names = request.POST.get('counters_names')

        house = houses.objects.get(id=request.session['house_id'])
        meeting = meetings.objects.get(meeting_id=request.session['meeting_id'])
        elect = elections.choose_elements(house_id=request.session['house_id'], meeting_id = meeting.meeting_id)
        context = {
                    'house': house,
                    'meeting_view' : meeting_view,
                    'date': str(datetime.datetime.now().date()),
                    'elections': elect,
                    'type_of_meeting': type_of_meeting,
                    'meeting': meeting,
                    'initiator_name': initiator_name,
                    'chairman_name': chairman_name,
                    'secretary_name': secretary_name,
                    'counters_names': counters_names,
                    'notification': notify,
                   }
        
        doc = DocxTemplate("protocol.docx")
        doc.render(context)
        now = datetime.datetime.now()
        filename = f"{now.strftime('%Y-%m-%d_%H-%M-%S')}_{uuid.uuid4().hex}.docx"
        buffer = BytesIO()
        doc.save(buffer)
        docx_file = ContentFile(buffer.getvalue())
        instance = protocol()
        instance.protocol_file.save(filename, docx_file, save=True)
        meeting.stage = 6
        meeting.protocol = instance
        meeting.save()
        link = "/construct/meeting/?id=" + str(meeting.meeting_id)
        add_new = news()
        add_new.news_text = "Собрание под названием " + meeting.title + " завершено. Вы можете посмотреть информацию об этом собрании, нажав на новость."
        add_new.house_id = meeting.house_id
        add_new.meeting = meeting
        add_new.need_link = True
        add_new.save()
        return redirect(link)
    else:
        return render(request, 'add_protocol.html', context={})
    

def download_file(request, file_path):
    file_name = os.path.basename(file_path)
    print(file_path)
    with open(file_path, 'rb') as file:
        response = FileResponse(file)
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
    
def get_notification_file(request):
    meeting = meetings.objects.get(meeting_id = request.session['meeting_id'])
    cur_notification = meeting.notification
    return FileResponse(cur_notification.notification_file)

def get_statement_file(request):
    meeting = meetings.objects.get(meeting_id = request.session['meeting_id'])
    cur_statement = meeting.statement
    return FileResponse(cur_statement.statement_file)

def get_protocol_file(request):
    meeting = meetings.objects.get(meeting_id = request.session['meeting_id'])
    cur_protocol = meeting.protocol
    return FileResponse(cur_protocol.protocol_file)


