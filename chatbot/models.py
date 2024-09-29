from django.db import models


class UploadedFile(models.Model):
    file_id = models.CharField(max_length=100, unique=True)
    file_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="uploaded")  # uploaded, processed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name
