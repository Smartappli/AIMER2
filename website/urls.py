from django.urls import path

from .views import (
    CustomDashboardView,
)

app_name = "website"

urlpatterns = [
    path("", CustomDashboardView.as_view(), name="dashboard"),
    path("", CustomDashboardView.as_view(), name="index"),
]
