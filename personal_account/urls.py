from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index_account, name='account'),
    re_path(r'^logout/$', views.account_logout, name='logout'),
    re_path(r'^new_user/$', views.new_user_account, name='new_user'),
]