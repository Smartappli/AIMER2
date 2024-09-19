from django.views.generic import TemplateView

from AIMER2 import TemplateLayout
from AIMER2.template_helpers.theme import TemplateHelper


class SystemView(TemplateView):
    template_name = "pages/system/not-found.html"
    status = None

    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Define the layout for this module
        # _templates/layout/system.html
        context.update(
            {
                "layout_path": TemplateHelper.set_layout(
                    "system.html",
                    context,
                ),
                "status": self.status,
            },
        )

        return context

    def render_to_response(self, context, **response_kwargs):
        # If a status is defined, it is added to the response arguments
        if self.status is not None:
            response_kwargs["status"] = self.status
        return super().render_to_response(context, **response_kwargs)


# Custom error views
def custom_404_view(request, exception):
    view = SystemView.as_view(template_name="pages/pages_misc_error.html")
    return view(request, status=404)


def custom_403_view(request, exception):
    view = SystemView.as_view(
        template_name="pages/pages_misc_not_authorized.html"
    )
    return view(request, status=403)


def custom_400_view(request, exception):
    view = SystemView.as_view(template_name="pages/pages_misc_error.html")
    return view(request, status=400)


def custom_500_view(request):
    view = SystemView.as_view(template_name="pages/pages_misc_error.html")
    return view(request, status=500)
