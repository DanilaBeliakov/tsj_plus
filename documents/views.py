from django.shortcuts import render
import sys
import os
sys.path.append(os.getcwd())
from construct.models import meetings
from authorization.models import houses

def index_documents(request):
    now_house = houses.objects.get(id=request.session['house_id'])
    my_meetings = meetings.objects.filter(house_id = now_house.id )
    return render(request,
                      'index_documents.html',
                      context={'my_meetings':my_meetings})

def doc_notes(request):
    now_house = houses.objects.get(id=request.session['house_id'])
    my_meetings = meetings.objects.filter(house_id = now_house.id )
    return render(request,
                      'doc_notes.html',
                      context={'my_meetings':my_meetings})

def doc_statements(request):
    now_house = houses.objects.get(id=request.session['house_id'])
    my_meetings = meetings.objects.filter(house_id = now_house.id )
    return render(request,
                      'doc_statements.html',
                      context={'my_meetings':my_meetings})

def doc_protocols(request):
    now_house = houses.objects.get(id=request.session['house_id'])
    my_meetings = meetings.objects.filter(house_id = now_house.id )
    return render(request,
                      'doc_protocols.html',
                      context={'my_meetings':my_meetings})