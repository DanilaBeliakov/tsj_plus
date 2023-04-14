from django.db import models
from django.urls import reverse
from django.http import HttpResponse
import sys
import os
sys.path.append(os.getcwd())
from construct.models import meetings
from authorization.models import users, houses

# Create your models here.
class news(models.Model):
    
    news_id = models.BigAutoField(primary_key = True)
    news_text = models.TextField()
    house_id = models.IntegerField()
    meeting = models.ForeignKey(meetings, on_delete=models.CASCADE, null=True, blank=True)
    need_link = models.BooleanField(default=False)

    
            


            