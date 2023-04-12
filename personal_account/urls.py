from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index_account, name='account'),
    re_path(r'^logout/$', views.account_logout, name='logout'),
    re_path(r'^new_user/$', views.new_user_account, name='new_user'),
    re_path(r'^change/$', views.change_user_data, name='change'),
    re_path(r'^tsj_data/$', views.save_tsj_data, name='tsj_data'),
]