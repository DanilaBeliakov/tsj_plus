from django.contrib import admin
from .models import votes, elections

admin.site.register(votes)
admin.site.register(elections)

