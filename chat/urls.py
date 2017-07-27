from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^register/$', views.registration, name='registration'),

    url(r'^chat/$', login_required(views.chat_room), name='chat_room'),
]
