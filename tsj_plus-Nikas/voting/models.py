from django.db import models
from django.urls import reverse
from django.http import HttpResponse

# Create your models here.
class votes(models.Model):

    vote_id = models.BigAutoField(primary_key = True)
    user_id = models.IntegerField()
    
    user_email = models.EmailField()
    user_name = models.CharField(max_length=50)
    user_flat= models.IntegerField()

    election_id = models.IntegerField()
    result = models.BooleanField()

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.vote_id)])

    def __str__(self):
        return self.user_name
    
    def choose_elements(election):
        elements = votes.objects.filter(election_id = election)
        res = []
        for elem in elements:
            res.append(elem)
        return res

    def voited_for(election):
        elements = votes.objects.filter(election_id = election, result = True)
        res = []
        for elem in elements:
            res.append(elem)
        return len(res)

    def voited_against(election):
        elements = votes.objects.filter(election_id = election, result = False)
        res = []
        for elem in elements:
            res.append(elem)
        return len(res)

class elections(models.Model):

    election_id = models.BigAutoField(primary_key = True)
    question = models.TextField()
    voited_for = models.IntegerField(default = 0)
    voited_against = models.IntegerField(default = 0)
    house_id = models.IntegerField(default = 0)

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.election_id)])

    def __str__(self):
        return self.question
    
    def choose_elements(house):
        elements = elections.objects.filter(house_id = house)
        res = []
        for elem in elements:
            res.append(elem)
        return res