from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisteByEmailView.as_view(),name='register'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('email-verify/', VerifyEmail.as_view(),name='email-verify'),
]