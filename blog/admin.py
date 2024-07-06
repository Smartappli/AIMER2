"""
Admin configuration for the Post and Comment models.

This module registers the Post and Comment models with the Django admin site
and customizes their admin interface.

Classes:
    PostAdmin: Customizes the admin interface for the Post model.
        - list_display: Fields to display in the list view.
        - list_filter: Fields to filter the list view.
        - search_fields: Fields to search in the list view.
        - prepopulated_fields: Fields to auto-fill based on other fields.
        - raw_id_fields: Fields to use a raw ID widget for.
        - date_hierarchy: Field to use for date drill-down navigation.
        - ordering: Default ordering of the list view.
        - show_facets: Facets display settings in the admin interface.

    CommentAdmin: Customizes the admin interface for the Comment model.
        - list_display: Fields to display in the list view.
        - list_filter: Fields to filter the list view.
        - search_fields: Fields to search in the list view.

Attributes:
    admin (module): The Django admin module for registering models.
    Comment (class): The Comment model class.
    Post (class): The Post model class.
"""
from django.contrib import admin

from .models import Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "publish", "status"]
    list_filter = ["status", "created", "publish", "author"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]
    date_hierarchy = "publish"
    ordering = ["status", "publish"]
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "post", "created", "active"]
    list_filter = ["active", "created", "updated"]
    search_fields = ["name", "email", "body"]
