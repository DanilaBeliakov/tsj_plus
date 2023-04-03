from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index_documents, name='index_documents'),
    re_path(r'^protocols/$', views.only_protocols, name='protocols'),
    re_path(r'^codex/$', views.only_codex, name='codex'),
]