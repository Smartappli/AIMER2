from django.urls import path
from .views import upload_and_process_files, UploadPage  # Correct the import here

app_name = "assistant"

urlpatterns = [
    path('upload-page/', UploadPage.as_view(), name='upload_page'),  # Use UploadPage instead of upload_page
    path('upload/', upload_and_process_files, name='upload_files'),
]