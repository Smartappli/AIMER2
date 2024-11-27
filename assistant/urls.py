from django.urls import path

from .views import (  # Correct the import here
    UploadPage,
    upload_and_process_files,
)

app_name = "assistant"

urlpatterns = [
    path("upload-page/", UploadPage.as_view(), name="upload_page"),  # Use UploadPage instead of upload_page
    path("upload/", upload_and_process_files, name="upload_files"),
]
