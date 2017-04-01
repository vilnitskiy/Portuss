from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^car-rent/', views.CarRentView.as_view(), name='car_rent'),
]
