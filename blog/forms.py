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
    """
    A form for sending an email about a post.

    Fields:
        name (CharField): The sender's name, with a maximum length of 25 characters.
        email (EmailField): The sender's email address.
        to (EmailField): The recipient's email address.
        comments (CharField): Optional comments, with a Textarea widget.
    """

    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea,
    )


class CommentForm(forms.ModelForm):
    """
    A ModelForm for creating and updating comments.

    Fields:
        name (CharField): The name of the commenter.
        email (EmailField): The email address of the commenter.
        body (CharField): The comment text.

    Meta:
        model (Comment): The model associated with this form.
        fields (list): The list of fields to include in the form.
    """

    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
