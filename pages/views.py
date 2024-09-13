from django.shortcuts import render
from django.views.generic import TemplateView, View
from pycaret.anomaly import models as get_anomaly_models
from timm import list_models, list_modules

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
        # A function to init the global layout. It is defined in AIMER2/__init__.py file
        return TemplateLayout.init(self, super().get_context_data(**kwargs))


class MiscPagesView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in AIMER2/__init__.py file
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


class CustomMLAnomalyView(PagesView, View):
    template_name = "pages/pages_machine_learning_anomaly_detection.html"

    def get(self, request, *args, **kwargs):
        # Retrieve the context of `FaqsView`
        context = self.get_context_data(**kwargs)
        context["models"] = get_anomaly_models()

        return render(request, self.template_name, context)


class CustomDPClassificationView(PagesView, View):
    template_name = "pages/pages_deep_learning_classification.html"

    def get(self, request, *args, **kwargs):
        modules_with_models = {
            module: sorted(list_models(module=module))
            for module in sorted(list_modules())
        }

        # Retrieve the context of `FaqsView`
        context = self.get_context_data(**kwargs)
        context["modules_with_models"] = modules_with_models

        return render(request, self.template_name, context)
