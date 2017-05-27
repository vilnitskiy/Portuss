from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
    url(
        r'^$',
        views.main,
        name='main'),
    url(
        r'^car-rent/$',
        login_required(views.CarRentView.as_view()),
        name='car_rent'),
    url(
        r'^profile/$',
        login_required(views.user_profile),
        name='user_profile'),
    url(
        r'^search/$',
        views.search,
        name='search'),
    url(
        r'^header-search/$',
        views.header_search,
        name='header_search'),
    url(
        r'^book-a-car/(?P<car_id>[0-9]+)/$',
        login_required(views.book_a_car),
        name='book_a_car'),
    url(
        r'^complete-booking/$',
        views.complete_booking,
        name='complete_booking'),

    # auth views
    url(r'^registration/',
        views.RegistrationView.as_view(),
        name='registration'),
    url(
        r'^logout/$',
        auth_views.logout,
        {'next_page': 'main'},
        name='logout'),
]
