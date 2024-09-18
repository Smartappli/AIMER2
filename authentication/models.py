from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django_cryptography.fields import encrypt


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    email = models.EmailField(
        max_length=100, unique=True
    )  # Use unique=True for unique email addresses
    date_of_birth = encrypt(models.DateField(blank=True, null=True))
    photo = encrypt(
        models.ImageField(
            upload_to="users/%Y/%m/%d/",
            blank=True,
        )
    )
    bio = encrypt(models.TextField(blank=True))
    email_token = models.CharField(max_length=100, blank=True)
    forget_password_token = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    def __str__(self):
        return self.user.username


# Signal receiver to create a Profile when a User is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            email=instance.email,
            date_of_birth=(
                instance.profile.date_of_birth
                if hasattr(instance, "profile")
                else None
            ),
            photo=(
                instance.profile.photo if hasattr(instance, "profile") else None
            ),
            bio=instance.profile.bio if hasattr(instance, "profile") else "",
        )


# Signal receiver to save the Profile whenever the User is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
