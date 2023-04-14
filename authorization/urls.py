from django.urls import path, re_path
from . import views


urlpatterns = [
    # path('', views.index_documents, name='index'),
    path('auth/', views.auth_page, name='auth'),
    path('signup/', views.sign_up_page, name='signup'),
    path('personal_info/', views.personal_data_page, name='personal_info'),
]