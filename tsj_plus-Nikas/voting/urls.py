from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index_voting, name='index_voting'),
    re_path(r'^add_voting/$', views.add_voting, name='add_voting'),
]