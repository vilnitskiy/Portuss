from django.conf.urls import url
from .views import index, liveblog


urlpatterns = [
    url(r'^chose-chat/', index),
    url(r'^liveblog/(?P<slug>[^/]+)/$', liveblog),
]
