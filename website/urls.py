from django.urls import include, path

from . import views

app_name = "website"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path('edit/', views.edit, name="edit"),
]
