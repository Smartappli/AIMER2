from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views
from .views import CustomFaqCategoryView

app_name = "faq"

urlpatterns = [
    path(
        "",
        login_required(CustomFaqCategoryView.as_view()),
        name="faq",
    ),
]
