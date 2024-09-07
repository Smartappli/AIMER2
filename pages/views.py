from django.views.generic import TemplateView

from AIMER2 import TemplateLayout
from AIMER2.template_helpers.theme import TemplateHelper

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to pages/urls.py file for more pages.
"""


class PagesView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        return TemplateLayout.init(self, super().get_context_data(**kwargs))


class MiscPagesView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Update the context
        context.update(
            {
                "layout_path": TemplateHelper.set_layout(
                    "layout_blank.html",
                    context,
                ),
            },
        )

        return context
