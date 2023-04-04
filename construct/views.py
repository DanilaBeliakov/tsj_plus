from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
import datetime
from django.utils.dateparse import parse_datetime
import sys
import os
from .models import meetings
sys.path.append(os.getcwd())

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