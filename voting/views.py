from django.shortcuts import render
from .models import votes, elections, offline_votes
from django.http import HttpResponseRedirect, HttpResponseNotFound
import datetime
from django.utils.dateparse import parse_datetime
import sys
import os
sys.path.append(os.getcwd())
from authorization.models import users, houses
from construct.models import meetings


def index_voting(request):
    if request.method == "POST":
        vote = votes()
        elect = request.POST.get('election_id')
        now_election = elections.objects.get(election_id=elect)
        now_user = users.objects.get(email=request.session['email'])
        vote.user = now_user
        vote.election = now_election
        now_vote = request.POST.get('vote')
        if now_vote == "ЗА":
            vote.result = 1
            now_election.voited_for_area += now_user.flat_area * now_user.flat_share
            now_election.voited_for_part = (now_election.voited_for_area / now_election.house.house_area)*100
        elif now_vote == "ПРОТИВ":
            vote.result = 0
            now_election.voited_against_area += now_user.flat_area * now_user.flat_share
            now_election.voited_against_part = (now_election.voited_against_area / now_election.house.house_area)*100
        else:
            vote.result = 2
            now_election.voited_idk_area += now_user.flat_area * now_user.flat_share
            now_election.voited_idk_part = (now_election.voited_idk_area / now_election.house.house_area)*100
        if (now_election.voited_for_part + now_election.voited_against_part + now_election.voited_idk_part) >= now_election.quorum_limit:
             now_election.is_quorum = 1
        else:
            now_election.is_quorum = 0
        vote.save()
        now_election.save()
    
    all_meetings = meetings.objects.filter(house_id = request.session['house_id'])
    my_meetings = []
    now_user = users.objects.get(email = request.session['email'])
    only_meetings = []
    for meeting in all_meetings:
        temp = elections.aviable(house_id = request.session['house_id'], meeting_id = meeting.meeting_id)
        my_votes = []
        for elem in temp:
            if not(votes.is_voted(user_id = now_user.user_id, election_id = elem.election_id)):
                my_votes.append(elem)
        if len(my_votes) > 0:
            my_meetings.append(my_votes)
    only_meetings.reverse()
    return render(
            request,
            'index_voting.html',
            context={"my_meetings": my_meetings, "now_user" : now_user},
    )

    
def voting_results(request):
    if request.method == "POST":
        now_vote = offline_votes.objects.get(vote_id = request.POST.get('vote_id'))
        now_election = elections.objects.get(election_id = request.POST.get('election_id'))

        if now_vote.result == 1:
            now_election.voited_for_area -= now_vote.user_flat_area * now_vote.user_flat_share
            now_election.voited_for_part = (now_election.voited_for_area / now_election.house.house_area)*100
        elif now_vote.result == 0:
            now_election.voited_against_area -= now_vote.user_flat_area * now_vote.user_flat_share
            now_election.voited_against_part = (now_election.voited_against_area / now_election.house.house_area)*100
        else:
            now_election.voited_idk_area -= now_vote.user_flat_area * now_vote.user_flat_share
            now_election.voited_idk_part = (now_election.voited_idk_area / now_election.house.house_area)*100

        if (now_election.voited_for_part + now_election.voited_against_part + now_election.voited_idk_part) >= now_election.quorum_limit:
            now_election.is_quorum = 1
        else:
            now_election.is_quorum = 0

        now_vote.delete()
        now_election.save()

    meeting_id = request.GET.get('id')
    meeting = meetings.objects.get(meeting_id=meeting_id)

    now_votes = []
    only_elections = []
    my_elections = elections.choose_elements(house_id = meeting.house_id, meeting_id = meeting.meeting_id)
    for elem in my_elections:
        only_elections.append(elem)
        temp =[]
        temp.append(elem)

        election_votes = votes.choose_elements(election = elem.election_id)
        for i in election_votes:
            temp.append(i)

        offline_election_votes = offline_votes.choose_elements(election = elem.election_id)
        for i in offline_election_votes:
            temp.append(i)
        now_votes.append(temp)

    only_elections.reverse()
    now_votes.reverse()
    return render(
            request,
            'voting_results.html',
            context ={"now_votes": now_votes,'meeting': meeting, "only_elections" : only_elections},
    )

def add_offline_votes(request):
    if request.method == "POST":
        meeting_id = request.GET.get('id')
        meeting = meetings.objects.get(meeting_id=meeting_id)
        now_house = houses.objects.get(id=request.session['house_id'])
        now_elections = elections.aviable(house_id = now_house.id, meeting_id = meeting.meeting_id)
        for now_election in now_elections:

            off_vote = offline_votes()
            off_vote.user_name = request.POST.get('user_name')
            off_vote.user_flat_number = int(request.POST.get('user_flat_number'))
            off_vote.user_flat_area = float(request.POST.get('user_flat_area'))
            off_vote.user_flat_share = float(request.POST.get('user_flat_share'))
            off_vote.election = now_election
            meeting_id = request.GET.get('id')

            ses = str(now_election.election_id)
            now_vote = request.POST.get(ses)

            if now_vote == "ЗА":
                off_vote.result = 1
                now_election.voited_for_area += off_vote.user_flat_area * off_vote.user_flat_share
                now_election.voited_for_part = (now_election.voited_for_area / now_election.house.house_area)*100
            elif now_vote == "ПРОТИВ":
                off_vote.result = 0
                now_election.voited_against_area += off_vote.user_flat_area * off_vote.user_flat_share
                now_election.voited_against_part = (now_election.voited_against_area / now_election.house.house_area)*100
            else:
                off_vote.result = 2
                now_election.voited_idk_area += off_vote.user_flat_area * off_vote.user_flat_share
                now_election.voited_idk_part = (now_election.voited_idk_area / now_election.house.house_area)*100
            if (now_election.voited_for_part + now_election.voited_against_part + now_election.voited_idk_part) >= now_election.quorum_limit:
                now_election.is_quorum = 1
            else:
                now_election.is_quorum = 0
            off_vote.save()
            now_election.save()

    my_meetings = []
    meeting_id = request.GET.get('id')
    meeting = meetings.objects.get(meeting_id=meeting_id)
    my_votes = elections.aviable(house_id = request.session['house_id'],meeting_id = meeting.meeting_id)
    return render(
            request,
            'add_offline.html',
            context = {"my_votes" : my_votes, "meeting" : meeting},
    )


