from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import FaqView

app_name = "faq"

urlpatterns = [
    path(
        "",
        login_required(FaqView.as_view(template_name="pages/pages_faq.html")),
        name="faq",
    ),
]
