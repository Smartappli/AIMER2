from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class Member(admin.ModelAdmin):
    list_display = (
        "user",
        "email",
        "is_verified",
        "created_at",
    )
