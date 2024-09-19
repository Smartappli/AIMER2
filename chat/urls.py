from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path(
        "room/<int:course_id>/",
        login_required(views.course_chat_room),
        name="course_chat_room",
    ),
    path(
        "support/<int:ticket_id>/",
        login_required(views.support_chat_room),
        name="support_chat_room",
    ),
]
