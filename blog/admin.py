"""Admin configuration for the Post and Comment models.

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

Attributes
----------
    admin (module): The Django admin module for registering models.
    Comment (class): The Comment model class.
    Post (class): The Post model class.

"""

from typing import ClassVar

from django.contrib import admin

from .models import Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin configuration for the Post model.

    Customizes the admin interface for the Post model with the following options:

    Attributes
    ----------
        list_display (list): Fields to display in the list view.
        list_filter (list): Fields to filter the list view.
        search_fields (list): Fields to search in the list view.
        prepopulated_fields (dict): Fields to auto-fill based on other fields.
        raw_id_fields (list): Fields to use a raw ID widget for.
        date_hierarchy (str): Field to use for date drill-down navigation.
        ordering (list): Default ordering of the list view.
        show_facets (ShowFacets): Facets display settings in the admin interface.

    """

    list_display: ClassVar[list] = [
        "title",
        "slug",
        "author",
        "publish",
        "status",
    ]
    list_filter: ClassVar[list] = ["status", "created", "publish", "author"]
    search_fields: ClassVar[list] = ["title", "body"]
    prepopulated_fields: ClassVar[dict] = {"slug": ("title",)}
    raw_id_fields: ClassVar[list] = ["author"]
    date_hierarchy = "publish"
    ordering: ClassVar[list] = ["status", "publish"]
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin configuration for the Comment model.

    Customizes the admin interface for the Comment model with the following options:

    Attributes
    ----------
        list_display (list): Fields to display in the list view.
        list_filter (list): Fields to filter the list view.
        search_fields (list): Fields to search in the list view.

    """

    list_display: ClassVar[list] = [
        "name",
        "email",
        "post",
        "created",
        "active",
    ]
    list_filter: ClassVar[list] = ["active", "created", "updated"]
    search_fields: ClassVar[list] = ["name", "email", "body"]
