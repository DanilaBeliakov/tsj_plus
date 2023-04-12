from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index_documents, name='index_documents'),
    re_path(r'^doc.notes/$', views.doc_notes, name='doc_notes'),
    re_path(r'^doc.statements/$', views.doc_statements, name='doc_statements'),
    re_path(r'^doc.protocols/$', views.doc_protocols, name='doc_protocols'),
]