from django.urls import path

from .views import (
    CustomDashboardView,
    CustomEditView,
    CustomLoginView,
    CustomLogoutView,
    CustomPasswordChangeDoneView,
    CustomPasswordChangeView,
    CustomPasswordResetCompleteView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetDoneView,
    CustomPasswordResetView,
    CustomRegisterView,
)

app_name = "website"

urlpatterns = [
    path("", CustomDashboardView.as_view(), name="dashboard"),
    path("", CustomDashboardView.as_view(), name="index"),
    path(
        "edit/",
        CustomEditView.as_view(),
        name="edit",
    ),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path(
        "password-change/",
        CustomPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password-change/done/",
        CustomPasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path(
        "password-reset/",
        CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "register/",
        CustomRegisterView.as_view(),  # Corrected to CustomRegisterView
        name="register",
    ),
]
