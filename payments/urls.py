from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'payment/token/', views.CheckoutView.as_view(), name='checkout'),
]
