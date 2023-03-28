from django.db import models
from django.urls import reverse
from django.http import HttpResponse

# Create your models here.
class news(models.Model):

    news_id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 30)
    news_text = models.TextField()
    type = models.CharField(max_length = 20)
    election_id = models.IntegerField()
    house_id = models.IntegerField()
    news_date = models.DateField()

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        return self.name
    
    def choose_elements(now_type, now_house):
        elements = news.objects.filter(type = now_type, house_id = now_house).order_by('-news_date')
        res = []
        for elem in elements:
            res.append(elem)
        return res
    
    def all_elements(now_house):
        elements = news.objects.filter(house_id = now_house).order_by('-news_date')
        res = []
        for elem in elements:
            res.append(elem)
        return res
            


            