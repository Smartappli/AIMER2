import csv
import datetime
from typing import ClassVar

from django.contrib import admin
from django.http import HttpResponse

from .models import Profile


@admin.action(description="Export to CSV")
def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta  # noqa: SLF001
    content_disposition = f"attachment; filename={opts.verbose_name_plural}.csv"
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = content_disposition
    writer = csv.writer(response)
    fields = [
        field
        for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many
    ]

    # Write the first row with header information
    writer.writerow([field.verbose_name for field in fields])

    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%Y-%m-%d %H:%M:%S")
            data_row.append(value)
        writer.writerow(data_row)
    return response


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Customizes the Django admin interface for the Profile model.

    Attributes
    ----------
        list_display (tuple): Specifies the fields of the Profile model to be displayed in the admin list view.
        list_filter (tuple): Specifies the fields of the Profile model to be used for filtering the list in the admin interface.

    """

    list_display = ("user", "date_of_birth", "photo")
    list_filter = ("user",)
    actions: ClassVar[list] = [export_to_csv]
