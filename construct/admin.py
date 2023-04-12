from django.contrib import admin
from .models import meetings, temp_elections, notification, statement

# Register your models here.
admin.site.register(meetings)
admin.site.register(temp_elections)
admin.site.register(notification)
admin.site.register(statement)