
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'MpesaPayments'

urlpatterns= [
    path('bookroom/payment/', views.bookingAndpayment, name="bookingAndpayment"),
    path('callback', views.call_back, name="call_back"),
]

