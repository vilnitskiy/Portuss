from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'payment/token/', views.start_payment_view, name='checkout'),
]
