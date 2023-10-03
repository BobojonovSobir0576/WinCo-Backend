from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisteByEmailView.as_view(),name='register'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('email-verify/', VerifyEmail.as_view(),name='email-verify'),
    path('detail/', UserDetailView.as_view(),name='detail'),
    path('request-rest-email/', RequestPasswordRestEmail.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckView.as_view(), name='password-reset-confirm'),
    path('reset_password_complete/', SetNewPasswordView.as_view(), name ='password_reset_complete'),

    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('reset_password/', PasswordResetView.as_view(), name ='reset_password'),
    # path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name ='password_reset_confirm'),
    # path('reset_password_complete/', PasswordResetCompleteView.as_view(), name ='password_reset_complete'),
]