from django.contrib import messages
from django.contrib.auth import alogin, authenticate
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView

from AIMER2 import TemplateLayout
from AIMER2.template_helpers.theme import TemplateHelper


class PagesView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in AIMER2/__init__.py file
        return TemplateLayout.init(self, super().get_context_data(**kwargs))


class WebsiteView(TemplateView):
    def get_context_data(self, **kwargs):
        # Get the base context from the parent class
        context = super().get_context_data(**kwargs)

        # Initialize the global layout using a function defined in AIMER2/__init__.py
        context = TemplateLayout.init(self, context)

        # Update the context with layout path
        context["layout_path"] = TemplateHelper.set_layout(
            "layout_blank.html", context
        )

        return context


class FrontPagesView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Update the context
        context.update({
            "layout": "front",
            "layout_path": TemplateHelper.set_layout(
                "layout_front.html", context
            ),
            "active_url": self.request.path,  # Get the current url path (active URL) from request
        })

        # map_context according to updated context values
        TemplateHelper.map_context(context)

        return context


@login_required
def dashboard(request):
    """Display the user dashboard.

    This view is only accessible to authenticated users. It renders the dashboard
    template with the 'section' context variable set to 'dashboard'.

    Args:
    ----
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
    -------
        HttpResponse: A response object with the rendered dashboard template.

    """
    return render(
        request,
        "pages/pages_dashboard.html",
    )


class CustomDashboardView(PagesView, View):
    template_name = "pages/pages_dashboard.html"

    def get(self, request, *args, **kwargs):
        # Retrieve the context of `PagesView`
        context = self.get_context_data(**kwargs)

        return render(request, self.template_name, context)
