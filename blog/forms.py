"""
Form definitions for the application.

This module defines forms for handling user input related to posts and comments.

Classes:
    EmailPostForm: A form for sending an email about a post.
        - name: The sender's name (CharField).
        - email: The sender's email address (EmailField).
        - to: The recipient's email address (EmailField).
        - comments: Optional comments (CharField with Textarea widget).

    CommentForm: A ModelForm for creating and updating comments.
        - Meta: Metadata for the form.
            - model: The Comment model.
            - fields: Fields to include in the form ("name", "email", "body").

Attributes:
    forms (module): The Django forms module for defining forms.
    Comment (class): The Comment model class.
"""
from django import forms

from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea,
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
