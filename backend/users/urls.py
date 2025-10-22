from django.urls import path
from .views import (
    UsernameAvailabilityView, RegisterView, VerifyOtpView,
    JwtLoginView, GoogleLoginView, ForgotPasswordRequestView,
    ResetPasswordView, ResendOtpView
)
from .views import GoogleLoginView  # Importing GoogleLoginView for URL routing

urlpatterns = [
    path("username-availability/", UsernameAvailabilityView.as_view()),
    path("register/", RegisterView.as_view()),
    path("verify-otp/", VerifyOtpView.as_view()),
    path("login/", JwtLoginView.as_view()),
    # path("google-login/", GoogleLoginView.as_view()),
    path("forgot-password/", ForgotPasswordRequestView.as_view()),
    path("reset-password/", ResetPasswordView.as_view()),
    path("resend-otp/", ResendOtpView.as_view()),  # ✅ new,
    path("google/", GoogleLoginView.as_view(), name="google-login"),
]
