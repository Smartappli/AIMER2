from typing import ClassVar

from django.contrib import admin

from .models import FaqCategory, FaqQuestion


@admin.register(FaqCategory)
class FaqCategoryAdmin(admin.ModelAdmin):
    list_display: ClassVar[list] = [
        "name",
        "slug",
        "icon",
    ]
    prepopulated_fields: ClassVar[dict] = {"slug": ("name",)}


@admin.register(FaqQuestion)
class FaqQuestionAdmin(admin.ModelAdmin):
    list_display: ClassVar[list] = [
        "title",
        "slug",
        "category",
        "body",
    ]
    prepopulated_fields: ClassVar[dict] = {"slug": ("title",)}
