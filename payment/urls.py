from django.urls import path
from . import views


urlpatterns = [
    path('create-checkout-session/', views.CreatePaymentIntetn.as_view()),
]