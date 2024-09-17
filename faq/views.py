from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, View
from taggit.models import Tag

from AIMER2 import TemplateLayout

from .models import FaqCategory, FaqQuestion


class FaqView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in AIMER2/__init__.py file
        return TemplateLayout.init(self, super().get_context_data(**kwargs))


class CustomFaqCategoryView(FaqView, View):
    template_name = "faq/faq.html"

    def get(self, request, *args, **kwargs):
        category_listing = FaqCategory.published.all()
        questions_listing = FaqQuestion.published2.all()

        # Retrieve the context of `FaqsView`
        context = self.get_context_data(**kwargs)
        context["categories"] = category_listing
        context["questions"] = questions_listing

        return render(request, self.template_name, context)
