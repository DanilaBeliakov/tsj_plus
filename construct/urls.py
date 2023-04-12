from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index_construct, name='index_construct'),
    re_path('meeting/', views.meeting_view, name='meeting_view'),
    re_path('add_meeting', views.add_meeting, name='add_meeting'),
    re_path('notification/', views.notification_view, name='notification_view'),
    re_path('add_statement/', views.add_statement, name='add_statement'),
    re_path('add_protocol/', views.add_protocol, name='add_protocol'),
    re_path('get_notification_file/', views.get_notification_file, name='get_notification_file'),
    re_path('get_statement_file/', views.get_statement_file, name='get_statement_file'),
    re_path('get_protocol_file/', views.get_protocol_file, name='get_protocol_file'),
]