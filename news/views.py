from django.shortcuts import render
from .models import news
from django.http import HttpResponseRedirect, HttpResponseNotFound
import datetime
from django.utils.dateparse import parse_datetime
import sys
import os
sys.path.append(os.getcwd())
from authorization.models import users


def index_news(request):
    now_user = users.objects.get(email = request.session['email'])
    all = news.all_elements(now_house = request.session['house_id'])

    return render(
            request,
            'index_news.html',
            context = {"all" : all, "now_user" : now_user},
    )

def only_notifications(request):
    now_user = users.objects.get(email = request.session['email'])
    type_y = news.choose_elements(now_type = "Уведомление", now_house = request.session['house_id'])
    return render(
            request,
            'notes.html',
            context = {"type_y" : type_y, "now_user" : now_user},
    )

def only_finals(request):
    now_user = users.objects.get(email = request.session['email'])
    type_i = news.choose_elements(now_type = "Итог собрания", now_house = request.session['house_id'])
    return render(
            request,
            'finals.html',
            context = {"type_i" : type_i, "now_user" : now_user},
    )

def create_news(request):

    if request.method == "POST":
        new = news()
        new.type = request.POST.get("type")
       # new.news_date = datetime.datetime.strptime(request.POST.get('date'),"%Y-%m-d%").date()
     #   new.news_date = parse_datetime(request.POST.get('date'))
        new.news_date = request.POST.get('date')
        new.news_text = ""
        new.election_id = -1
        new.house_id = request.session['house_id']
        if request.POST.get("type") == "Уведомление":
            new.name = "Уведомление от "+ request.POST.get('date')
        else:
            new.name = "Итог собрания от "+ request.POST.get('date')
        if request.POST.get("type") == "Уведомление":
            new.news_text = "Тут будет текст уведомления"
        else:
            new.news_text = "Тут будет текст итога собрания"
        new.save()
        return HttpResponseRedirect("/news")
    else:
        return render(
            request,
            'add_news.html',
            context = {},
        )

def block_construct(request):

    return render(
            request,
            'construct.html',
            context = {},
    )

