from django.shortcuts import render
from .models import votes, elections, offline_votes
from django.http import HttpResponseRedirect, HttpResponseNotFound
import datetime
from django.utils.dateparse import parse_datetime
import sys
import os
sys.path.append(os.getcwd())
from authorization.models import users, houses


def index_voting(request):

    if request.method == "POST":
        vote = votes()
        elect = request.POST.get('election_id')
        now_election = elections.objects.get(election_id = elect)
        now_user = users.objects.get(email = request.session['email'])
        vote.user = now_user
        vote.election = now_election
        now_vote = request.POST.get('vote')
        if now_vote == "ЗА":
            vote.result = 1
            now_election.voited_for_area += now_user.flat_area * now_user.flat_share
            now_election.voited_for_part = (now_election.voited_for_area / now_election.house.house_area)*100
        else:
            vote.result = 0
            now_election.voited_against_area += now_user.flat_area * now_user.flat_share
            now_election.voited_against_part = (now_election.voited_against_area / now_election.house.house_area)*100
        if (now_election.voited_for_part + now_election.voited_against_part) >= now_election.quorum_limit:
             now_election.is_quorum = 1
        else:
            now_election.is_quorum = 0
        vote.save()
        now_election.save()
    temp = elections.choose_elements(house_id = request.session['house_id'])
    now_user = users.objects.get(email = request.session['email'])
    my_votes = []
    for elem in temp:
        if not(votes.is_voted(user_id = now_user.user_id, election_id = elem.election_id)):
            my_votes.append(elem)
    my_votes.reverse()
    return render(
            request,
            'index_voting.html',
            context = {"my_votes" : my_votes, "now_user" : now_user},
    )

def add_voting(request):

    if request.method == "POST":
        now_house = houses.objects.get(id = request.session['house_id'])
        elect = elections()
        elect.question = request.POST.get('question')
        elect.voited_for_area = 0
        elect.voited_against_area = 0
        elect.voited_for_part = 0
        elect.voited_against_part = 0
        elect.house =now_house
        elect.save()
        return HttpResponseRedirect("/voting")
    else:
        return render(
            request,
            'add_voting.html',
            context = {},
        )
    
def voting_results(request):
    
    if request.method == "POST":
        now_vote = offline_votes.objects.get(vote_id = request.POST.get('vote_id'))
        now_election = elections.objects.get(election_id = request.POST.get('election_id'))

        if now_vote.result == 1:
            now_election.voited_for_area -= now_vote.user_flat_area * now_vote.user_flat_share
            now_election.voited_for_part = (now_election.voited_for_area / now_election.house.house_area)*100
        else:
            now_election.voited_against_area -= now_vote.user_flat_area * now_vote.user_flat_share
            now_election.voited_against_part = (now_election.voited_against_area / now_election.house.house_area)*100

        if (now_election.voited_for_part + now_election.voited_against_part) >= now_election.quorum_limit:
            now_election.is_quorum = 1
        else:
            now_election.is_quorum = 0

        now_vote.delete()
        now_election.save()

    my_elections = elections.choose_elements(house_id = request.session['house_id'])
    house_votes = []
    for elem in my_elections:
        temp = []
        temp.append(elem)

        election_votes = votes.choose_elements(election = elem.election_id)
        for i in election_votes:
            temp.append(i)

        offline_election_votes = offline_votes.choose_elements(election = elem.election_id)
        for i in offline_election_votes:
            temp.append(i)

        house_votes.append(temp)

    house_votes.reverse()
    return render(
            request,
            'voting_results.html',
            context ={"house_votes": house_votes},
    )

def add_offline_votes(request):
    if request.method == "POST":
        off_vote = offline_votes()
        off_vote.user_name = request.POST.get('user_name')
        off_vote.user_flat_number = int(request.POST.get('user_flat_number'))
        off_vote.user_flat_area = float(request.POST.get('user_flat_area'))
        off_vote.user_flat_share = float(request.POST.get('user_flat_share'))
        elect = request.POST.get('election_id')
        now_election = elections.objects.get(election_id = elect)
        off_vote.election = now_election
        now_vote = request.POST.get('vote')

        if now_vote == "ЗА":
            off_vote.result = 1
            now_election.voited_for_area += off_vote.user_flat_area * off_vote.user_flat_share
            now_election.voited_for_part = (now_election.voited_for_area / now_election.house.house_area)*100
        else:
            off_vote.result = 0
            now_election.voited_against_area += off_vote.user_flat_area * off_vote.user_flat_share
            now_election.voited_against_part = (now_election.voited_against_area / now_election.house.house_area)*100
        if (now_election.voited_for_part + now_election.voited_against_part) >= now_election.quorum_limit:
            now_election.is_quorum = 1
        else:
            now_election.is_quorum = 0
        off_vote.save()
        now_election.save()

    my_votes = elections.choose_elements(house_id = request.session['house_id'])
    my_votes.reverse()
    return render(
            request,
            'add_offline.html',
            context = {"my_votes" : my_votes},
    )


