"""
This module defines the database models for a blogging application, including
the `Post` and `Comment` models. The `Post` model includes a custom manager
for retrieving published posts.

Classes:
    PublishedManager: Custom manager for the `Post` model that retrieves only published posts.
    Post: Represents a blog post with various attributes like title, slug, author, body, and status.
    Comment: Represents a comment on a blog post, including the post it belongs to, the author's name and email, the comment body, and its status.

Functions:
    Post.get_absolute_url: Returns the URL to access a detail view of the blog post.
"""
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

class PublishedManager(models.Manager):
    """
    Custom manager to retrieve only published posts.

    Methods:
        get_queryset: Overrides the default queryset to filter posts by published status.
    """
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
    """
    Represents a blog post.

    Attributes:
        title (str): The title of the post.
        slug (str): The slug for the post, used in URLs.
        author (ForeignKey): The user who wrote the post.
        body (str): The content of the post.
        publish (datetime): The datetime when the post was published.
        created (datetime): The datetime when the post was created.
        updated (datetime): The datetime when the post was last updated.
        status (str): The publication status of the post (draft or published).
    
    Methods:
        get_absolute_url: Returns the URL to access a detail view of the post.
    """
    class Status(models.TextChoices):
        """
        Enumeration for post status.
        """
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_posts")
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns the URL to access a detail view of the post.

        Returns:
            str: URL to access the post detail view.
        """
        return reverse("blog:post_detail", args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

class Comment(models.Model):
    """
    Represents a comment on a blog post.

    Attributes:
        post (ForeignKey): The post that the comment is related to.
        name (str): The name of the comment author.
        email (EmailField): The email of the comment author.
        body (str): The content of the comment.
        created (datetime): The datetime when the comment was created.
        updated (datetime): The datetime when the comment was last updated.
        active (bool): The status indicating if the comment is active.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
