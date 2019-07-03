from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('zxc/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('invite/', include('invite.urls', namespace='invite')),
    path('labs/', include('labs.urls', namespace='labs')),
    path('sec/', include('sec.urls', namespace='sec'))
]
