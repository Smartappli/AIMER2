from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import (
    CustomDashboardView,
)

app_name = "website"

urlpatterns = [
    path("", login_required(CustomDashboardView.as_view()), name="dashboard"),
    path("", CustomDashboardView.as_view(), name="index"),
]
