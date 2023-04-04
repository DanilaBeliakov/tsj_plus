from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index_construct, name='index_construct'),
]