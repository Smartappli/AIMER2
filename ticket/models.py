from django.conf import settings
from django.db import models
from django.utils import timezone

class Post(models.Model):
    """
    Represents a post or ticket within the application.

    Attributes:
        title (str): The title of the post, limited to 250 characters.
        body (str): The content of the post.
        author (User): The user who authored the post, linked to the AUTH_USER_MODEL.
        closed (datetime): The date and time the post was closed, defaulting to the current time.
        created (datetime): The date and time the post was created, automatically set at creation.
        updated (datetime): The date and time the post was last updated, automatically set on save.
        status (str): The status of the post, with choices defined in the Status inner class.
    
    Methods:
        __str__(): Returns the title of the post as its string representation.
    
    Meta:
        ordering (list): Orders posts by the 'updated' field in descending order.
    """
    
    class Status(models.TextChoices):
        """
        Defines the possible statuses for a post.
        
        Attributes:
            DRAFT (tuple): Status for a draft post.
            SENT (tuple): Status for a sent post.
            OPEN (tuple): Status for an open post.
            IN_PROGRESS (tuple): Status for a post in progress.
            WAITING (tuple): Status for a post that is waiting.
            CLOSED (tuple): Status for a closed post.
            REOPENED (tuple): Status for a reopened post.
        """
        DRAFT = "DF", "Draft"
        SENT = "SS", "Sent"
        OPEN = "OP", "Open"
        IN_PROGRESS = "IP", "In Progress"
        WAITING = "WA", "Waiting"
        CLOSED = "CL", "Closed"
        REOPENED = "RE", "Reopened"

    title = models.CharField(max_length=250)
    body = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ticket_posts",
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
        ordering = ["-updated"]

    def __str__(self):
        return self.title
