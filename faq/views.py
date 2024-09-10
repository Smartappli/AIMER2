from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from taggit.models import Tag

from AIMER2 import TemplateLayout

from .models import FaqCategory, FaqQuestion


class FaqView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        return TemplateLayout.init(self, super().get_context_data(**kwargs))

def faq_list(request, tag_slug=None):
    category_listing = FaqCategory.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        category_listing = category_listing.filter(tags__in=[tag])
    return render(request, "pages/pages_faq.html", {"categories": category_listing, "tag": tag})
