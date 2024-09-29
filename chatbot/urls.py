from django.urls import path

from . import views

app_name = "chatbot"

urlpatterns = [
    path("chatbot/", views.chatbot_view, name="chatbot"),
    path("upload/", views.upload_view, name="upload"),
    path("process/", views.process_view, name="process_files"),
    path("delete/<str:file_id>/", views.delete_file_view, name="delete_file"),
]
