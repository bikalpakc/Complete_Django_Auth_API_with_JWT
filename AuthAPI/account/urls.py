from django.contrib import admin
from django.urls import path, include
from account.views import UserRegistrationView, UserLoginView, UserProfileView, UserChangePasswordView, SendPasswordResetEmailView, UserPasswordResetView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('profile/', UserProfileView.as_view(), name="profile"),
    path('change-password/', UserChangePasswordView.as_view(), name="change-password"),
    path('change-password/', UserChangePasswordView.as_view(), name="change-password"),
    path('send-password-reset-email/', SendPasswordResetEmailView.as_view(), name="send-password-reset-email"),
    path('password-reset/<uid>/<token>/', UserPasswordResetView.as_view(), name="password-reset"),
]
