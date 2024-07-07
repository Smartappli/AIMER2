from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Customizes the Django admin interface for the Profile model.

    Attributes:
        list_display (tuple): Specifies the fields of the Profile model to be displayed in the admin list view.
        list_filter (tuple): Specifies the fields of the Profile model to be used for filtering the list in the admin interface.
    """
    list_display = ("user", "date_of_birth", "photo")
    list_filter = ("user",)
