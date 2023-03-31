from django.urls import path, re_path, include
import authorization.views as auth
import documents.views as documents
import news.views as news
from django.contrib import admin
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', auth.auth_page, name='auth'),
    path('signup/', auth.sign_up_page, name='signup'),
    path('documents/', include('documents.urls')),
    path('news/', include('news.urls')),
    path('account/', include('personal_account.urls')),
    path('voting/', include('voting.urls'))
]

urlpatterns += [
    path('', RedirectView.as_view(url='/auth/', permanent=True)),
]