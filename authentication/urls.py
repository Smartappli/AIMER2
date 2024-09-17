from django.urls import path

from .views import (
    ForgetPasswordView,
    LoginView,
    LogoutView,
    RegisterView,
    ResetPasswordView,
    SendVerificationView,
    VerifyEmailTokenView,
    VerifyEmailView,
)

app_name = "authentication"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(template_name="auth/login.html"),
        name="auth-login",
    ),
    path(
        "logout/",
        LogoutView.as_view(template_name="auth/logged_out.html"),
        name="auth-logout",
    ),
    path(
        "register/",
        RegisterView.as_view(template_name="auth/register.html"),
        name="auth-register",
    ),
    path(
        "verify_email/",
        VerifyEmailView.as_view(template_name="auth/verify_email.html"),
        name="auth-verify-email-page",
    ),
    path(
        "verify/email/<str:token>/",
        VerifyEmailTokenView.as_view(),
        name="auth-verify-email",
    ),
    path(
        "reset_password/",
        ResetPasswordView.as_view(template_name="auth/reset_password.html"),
        name="auth-reset-password",
    ),
    path(
        "forgot_password/",
        ForgetPasswordView.as_view(template_name="auth/forgot_password.html"),
        name="auth-forgot-password",
    ),
    path(
        "send_verification/",
        SendVerificationView.as_view(),
        name="send-verification",
    ),
]
