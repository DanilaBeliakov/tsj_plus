from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index_construct, name='index_construct'),
    re_path('meeting/', views.meeting_view, name='meeting_view'),
]