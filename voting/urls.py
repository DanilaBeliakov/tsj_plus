from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index_voting, name='index_voting'),
    re_path(r'^voting_results/$', views.voting_results, name='voting_results'),
    re_path(r'^add_offline/$', views.add_offline_votes, name='add_offline'),
]