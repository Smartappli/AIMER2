from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        SENT = 'SS', 'Sent'
        OPEN = 'OP', 'Open'
        IN_PROGRESS = 'IP', 'In Progress'
        WAITING = 'WA', 'Waiting'
        CLOSED = 'CL', 'Closed'
        REOPENED = 'RE', 'Reopened'

    title = models.CharField(max_length=250)
    body = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ticket_posts'
    )
    closed = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.title
