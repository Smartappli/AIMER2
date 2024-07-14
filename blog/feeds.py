import markdown
from django.contrib.syndication.views import Feed
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy

from .models import Post


class LatestPostsFeed(Feed):
    title = _("AIMER Blog")
    link = reverse_lazy("blog:post_list")
    description = _("Latest News")

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item):
        return item.publish
