from django.contrib.sitemaps import Sitemap
from taggit.models import Tag
from django.urls import reverse
from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated


class TagSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Tag.objects.all()

    def location(self, item):
        return reverse('blog:post_list_by_tag', args=[item.slug])