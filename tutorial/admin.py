from typing import ClassVar

from django.contrib import admin

from .models import Course, Module, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display: ClassVar[dict] = ["title", "slug"]
    prepopulated_fields: ClassVar[dict] = {"slug": ("title",)}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display: ClassVar[list] = ["title", "subject", "created"]
    list_filter: ClassVar[list] = ["created", "subject"]
    search_fields: ClassVar[list] = ["title", "overview"]
    prepopulated_fields: ClassVar[dict] = {"slug": ("title",)}
    inlines: ClassVar[list] = [ModuleInline]
