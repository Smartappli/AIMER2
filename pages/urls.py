from django.urls import path

from .views import MiscPagesView

app_name = "pages"

urlpatterns = [
    path(
        "pages/misc/error/",
        MiscPagesView.as_view(template_name="pages/pages_misc_error.html"),
        name="pages-misc-error",
    ),
    path(
        "pages/misc/under_maintenance/",
        MiscPagesView.as_view(
            template_name="pages/pages_misc_under_maintenance.html",
        ),
        name="pages-misc-under-maintenance",
    ),
    path(
        "pages/misc/comingsoon/",
        MiscPagesView.as_view(template_name="pages/pages_misc_comingsoon.html"),
        name="pages-misc-comingsoon",
    ),
    path(
        "pages/misc/not_authorized/",
        MiscPagesView.as_view(
            template_name="pages/pages_misc_not_authorized.html",
        ),
        name="pages-misc-not-authorized",
    ),
]
