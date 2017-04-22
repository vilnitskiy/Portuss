from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^car-rent/', views.CarRentView.as_view(), name='car_rent'),

    # auth views
    url(r'^registration/',
        views.RegistrationView.as_view(),
        name='registration'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'main'}, name='logout'),
]
