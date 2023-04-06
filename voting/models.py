from django.db import models
from django.urls import reverse
from django.http import HttpResponse
import sys
import os
sys.path.append(os.getcwd())
from authorization.models import users,houses


class elections(models.Model):
    election_id = models.BigAutoField(primary_key = True)
    type = models.CharField(default = "Онлайн", max_length=10)
    question = models.TextField()
    voited_for_area = models.FloatField(default = 0)
    voited_against_area = models.FloatField(default = 0)
    voited_for_part = models.FloatField(default = 0)
    voited_against_part = models.FloatField(default = 0)
    house = models.ForeignKey(houses, on_delete=models.CASCADE)
    quorum_limit = models.FloatField(default = 50)
    is_quorum = models.BooleanField(default = False)
    

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.election_id)])

    def __str__(self):
        return self.question
    
    def choose_elements(house_id):
        elements = elections.objects.filter(house = houses.objects.get(id = house_id))
        res = []
        for elem in elements:
            res.append(elem)
        return res

# Create your models here.
class votes(models.Model):

    vote_id = models.BigAutoField(primary_key = True)

    user = models.ForeignKey(users, on_delete=models.CASCADE)

    election = models.ForeignKey(elections, on_delete=models.CASCADE)

    result = models.BooleanField()

    
    def choose_elements(election):
        elements = votes.objects.filter(election = elections.objects.get(election_id = election))
        res = []
        for elem in elements:
            res.append(elem)
        return res
    
    def is_voted(user_id, election_id):
        temp = votes.objects.filter(user = users.objects.get(user_id = user_id))
        for elem in temp:
            if elem.election.election_id == election_id:
                return True
        return False
    

class offline_votes(models.Model):
    vote_id = models.BigAutoField(primary_key = True)
    type = models.CharField(default = "Очное", max_length=10)
    user_name = models.CharField(max_length=50)
    user_flat_number = models.IntegerField(default = -1)
    user_flat_area = models.FloatField(default = 30)
    user_flat_share = models.FloatField(default = 1)
    election = models.ForeignKey(elections, on_delete=models.CASCADE)
    result = models.BooleanField()

    def choose_elements(election):
        elements = offline_votes.objects.filter(election = elections.objects.get(election_id = election))
        res = []
        for elem in elements:
            res.append(elem)
        return res
    
    def is_voted(election_id, user_name):
        temp = offline_votes.objects.filter(election = elections.objects.get(election_id = election_id))
        for elem in temp:
            if elem.user_name == user_name:
                return True
        return False


