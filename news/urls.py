from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index_news, name='index_news'),
    re_path(r'^meetings_news/$', views.meetings_news, name='meetings_news'),
    re_path(r'^other_news/$', views.other_news, name='other_news'),
    re_path(r'^add_news/$', views.create_news, name='add_news'),
]