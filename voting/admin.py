from django.contrib import admin
from .models import votes, elections,offline_votes

admin.site.register(votes)
admin.site.register(elections)
admin.site.register(offline_votes)

