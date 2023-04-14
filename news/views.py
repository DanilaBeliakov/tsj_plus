from django.shortcuts import render
from .models import news
from django.http import HttpResponseRedirect, HttpResponseNotFound
import datetime
from django.utils.dateparse import parse_datetime
import sys
import os
sys.path.append(os.getcwd())
from authorization.models import users,houses
from construct.models import meetings


def index_news(request):
    my_news = news.objects.filter(house_id = request.session['house_id']).order_by("-news_id")
    now_user = users.objects.get(email = request.session['email'])
    now_house = houses.objects.get(id = request.session['house_id'])
    
    return render(
            request,
            'index_news.html',
            context = {"my_news" : my_news, "now_user" : now_user, "now_house" : now_house},
    )


def meetings_news(request):
    my_news = news.objects.filter(house_id = request.session['house_id'], need_link = True).order_by("-news_id")
    now_user = users.objects.get(email = request.session['email'])
    now_house = houses.objects.get(id = request.session['house_id'])

    return render(
            request,
            'meetings_news.html',
            context = {"my_news" : my_news, "now_user" : now_user, "now_house" : now_house},
    )

def other_news(request):
    my_news = news.objects.filter(house_id = request.session['house_id'], need_link = False).order_by("-news_id")
    now_user = users.objects.get(email = request.session['email'])
    now_house = houses.objects.get(id = request.session['house_id'])

    return render(
            request,
            'other_news.html',
            context = {"my_news" : my_news, "now_user" : now_user, "now_house" : now_house},
    )

def create_news(request):

    if request.method == "POST":
        new = news()
       # new.news_date = datetime.datetime.strptime(request.POST.get('date'),"%Y-%m-d%").date()
       # new.news_date = parse_datetime(request.POST.get('date'))
        new.news_text = request.POST.get('editor1')
        new.house_id = request.session['house_id']
        # if request.POST.get("type") == "Уведомление":
        #     new.news_text = "Тут будет текст уведомления"
        # else:
        #     new.news_text = "Тут будет текст итога собрания"
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

