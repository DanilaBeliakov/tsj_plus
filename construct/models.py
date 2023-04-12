from django.db import models
import os
from django.conf import settings
base_path = os.path.join(settings.BASE_DIR, 'path', 'to', 'file')

# Create your models here.
class notification(models.Model):
    notification_id = models.BigAutoField(primary_key=True)
    type_of_voting = models.CharField(max_length=15)
    type_of_plans = models.CharField(max_length=15,default = "")
    place_of_meeting = models.CharField(max_length=100)
    date_of_start = models.CharField(max_length=30,default = "")
    date_of_end = models.CharField(max_length=30,default = "")
    time_of_start = models.CharField(max_length=30,default = "")
    time_of_end = models.CharField(max_length=30,default = "")
    notification_file = models.FileField(upload_to='files/notifications/', blank=True, null=True)

class statement(models.Model):
    statement_id = models.BigAutoField(primary_key=True)
    statement_file = models.FileField(upload_to='files/statements/', blank=True, null=True)

class protocol(models.Model):
    protocol_id = models.BigAutoField(primary_key=True)
    protocol_file = models.FileField(upload_to='files/protocol/', blank=True, null=True)

class meetings(models.Model):
    meeting_id = models.BigAutoField(primary_key=True)
    stage = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    date = models.DateField(default = '01-01-2000')
    house_id = models.IntegerField()
    notification = models.ForeignKey(notification, on_delete = models.CASCADE, null = True, blank = True)
    statement = models.ForeignKey(statement, on_delete = models.CASCADE, null = True, blank = True)
    protocol = models.ForeignKey(protocol, on_delete = models.CASCADE, null = True, blank = True)

    def all_elements(house):
        elements = meetings.objects.filter(house_id = house).order_by('-date')
        res = []
        for elem in elements:
            res.append(elem)
        return res
    

class temp_elections(models.Model):
    temp_id = models.BigAutoField(primary_key=True)
    question = models.TextField()
    house_id = models.IntegerField(default = 0)
    num_in_meeting = models.IntegerField(default = 0)

    def __str__(self):
        return self.question
    



    
