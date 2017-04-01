from django.conf.urls import url
from chat import views

urlpatterns = [
    url(r'^chat_main/$', views.about, name='about'),
    url(r'^new/$', views.new_room, name='new_room'),
    url(r'^chat/(?P<label>[\w-]{,50})/$', views.chat_room, name='chat_room'),
]
