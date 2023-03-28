from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index_news, name='index_news'),
    re_path(r'^notes/$', views.only_notifications, name='notes'),
    re_path(r'^finals/$', views.only_finals, name='finals'),
    re_path(r'^construct/$', views.block_construct, name='construct'),
    re_path(r'^personal/$', views.block_personal, name='personal'),
    re_path(r'^add_news/$', views.create_news, name='add_news'),
]