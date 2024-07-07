from django.conf import settings
from django.db import models


class Profile(models.Model):
    """
    Profile model to extend the default user model with additional fields.

    Attributes:
        user (OneToOneField): A one-to-one relationship with the user model specified in settings.AUTH_USER_MODEL.
                              This ensures each user has only one profile and each profile is related to a single user.
        date_of_birth (DateField): An optional date field to store the user's date of birth. Can be left blank or null.
        photo (ImageField): An optional image field to store the user's profile picture. The images are uploaded
                            to the directory specified by the 'upload_to' parameter, which organizes them by year,
                            month, and day.
        bio (TextField): An optional text field for the user to provide a short biography. Can be left blank or null.

    Methods:
        __str__(): Returns a string representation of the profile, displaying the associated user's username.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
    )
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(
        upload_to="users/%Y/%m/%d/",
        blank=True,
    )
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
