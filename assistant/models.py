import uuid

from django.contrib.auth import get_user_model
from django.db import models
from pgvector.django import VectorField

User = get_user_model()


class KnowledgeBase(models.Model):
    class AccessTypes(models.TextChoices):
        PUBLIC = "PU", "Public"
        PRIVATE = "PR", "Private"
        SHARED = "SH", "Shared"

    unique_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    original_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    file_type = models.CharField(max_length=4)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="knowledgebase"
    )
    access_type = models.CharField(max_length=2, choices=AccessTypes.choices)
    shared_with = models.ManyToManyField(User, related_name="shared_files")
    processed = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.original_name


class TextEmbedding(models.Model):
    class Status(models.TextChoices):
        NONE = "NO", "None"
        INPROGRESS = "IP", "In Progress"
        ERROR = "ER", "Error"
        DONE = "DN", "Done"

    file = models.ForeignKey(KnowledgeBase, on_delete=models.CASCADE)
    text_chunk = models.TextField()
    embedding_algorithm = models.CharField(max_length=50, default="llama3.2")
    embedding = VectorField(dimensions=3072)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.NONE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.original_name


class TableEmbedding(models.Model):
    class Status(models.TextChoices):
        NONE = "NO", "None"
        INPROGRESS = "IP", "In Progress"
        ERROR = "ER", "Error"
        DONE = "DN", "Done"

    file = models.ForeignKey(KnowledgeBase, on_delete=models.CASCADE)
    table_data = models.TextField()
    embedding_algorithm = models.CharField(max_length=50, default="llama3.2")
    embedding = VectorField(dimensions=3072)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.NONE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.original_name


class ImageEmbedding(models.Model):
    class Status(models.TextChoices):
        NONE = "NO", "None"
        INPROGRESS = "IP", "In Progress"
        ERROR = "ER", "Error"
        DONE = "DN", "Done"

    file = models.ForeignKey(KnowledgeBase, on_delete=models.CASCADE)
    image_data = models.TextField()
    embedding_algorithm = models.CharField(max_length=50, default="llama3.2")
    embedding = VectorField(dimensions=3072)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.NONE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.original_name
