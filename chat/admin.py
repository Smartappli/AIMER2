from typing import ClassVar

from django.contrib import admin

from chat.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display: ClassVar[list] = ["sent_on", "user", "course", "content"]
    list_filter: ClassVar[list] = ["sent_on", "course"]
    search_fields: ClassVar[list] = ["content"]
    raw_id_fields: ClassVar[list] = ["user", "course"]
