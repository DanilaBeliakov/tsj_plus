from django.db import models
from django.urls import reverse

# Create your models here.
class documents(models.Model):

    document_id = models.IntegerField(primary_key = True)
    document_text = models.TextField()
    name = models.CharField(max_length = 30)
    type = models.CharField(max_length = 20)
    house_id = models.IntegerField()
    document_date = models.DateField()

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of MyModelName.
        """
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        return self.name
    
    def choose_elements(now_type, now_house):
        elements = documents.objects.filter(type = now_type, house_id = now_house).order_by('-document_date')
        res = []
        for elem in elements:
            res.append(elem)
        return res
    
    def all_elements(now_house):
        elements = documents.objects.filter(house_id = now_house).order_by('-document_date')
        res = []
        for elem in elements:
            res.append(elem)
        return res
            


            