from django.db import models


# Create your models here.
class meetings(models.Model):
    meeting_id = models.BigAutoField(primary_key=True)
    stage = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    date = models.DateField()
    house_id = models.IntegerField()

    def all_elements(house):
        elements = meetings.objects.filter(house_id = house).order_by('-date')
        res = []
        for elem in elements:
            res.append(elem)
        return res