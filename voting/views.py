from django.shortcuts import render
from .models import votes, elections
from django.http import HttpResponseRedirect, HttpResponseNotFound
import datetime
from django.utils.dateparse import parse_datetime
import sys
import os
sys.path.append(os.getcwd())
from authorization.models import users


def index_voting(request):

    if request.method == "POST":
        vote = votes()
        elect = request.POST.get('election_id')
        now_election = elections.objects.get(election_id = elect)
        now_user = users.objects.get(email = request.session['email'])
        vote.user_id = now_user.user_id
        vote.user_email = now_user.email
        vote.user_name = now_user.full_name
        vote.user_flat = now_user.flat_number
        vote.election_id = now_election.election_id
        now_vote = request.POST.get('vote')
        if now_vote == "ЗА":
            vote.result = 1
            now_election.voited_for += 1
        else:
            vote.result = 0
            now_election.voited_against += 1
        vote.save()
        now_election.save()
    
    temp = elections.choose_elements(house = request.session['house_id'])
    now_user = users.objects.get(email = request.session['email'])
    my_votes = []
    for elem in temp:
        if not(votes.objects.filter(user_id = now_user.user_id, election_id = elem.election_id).exists()):
            my_votes.append(elem)
    return render(
            request,
            'index_voting.html',
            context = {"my_votes" : my_votes, "now_user" : now_user},
    )

def add_voting(request):

    if request.method == "POST":
        elect = elections()
        elect.question = request.POST.get('question')
        elect.voted_for = 0
        elect.voted_against = 0
        elect.house_id = request.session['house_id']
        elect.save()
        return HttpResponseRedirect("/voting")
    else:
        return render(
            request,
            'add_voting.html',
            context = {},
        )
