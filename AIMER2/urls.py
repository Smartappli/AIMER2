"""URL configuration for AIMER2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/

Examples
--------
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.utils.translation import gettext_lazy as _

from AIMER2.views import (
    custom_400_view,
    custom_403_view,
    custom_404_view,
    custom_500_view,
)
from blog.sitemaps import PostSitemap, TagSitemap

admin.site.site_header = _("AIMER Administration")
admin.site.site_title = _(
    "Artificial Intelligence for Medical Research - Portal Administration",
)
admin.site.index_title = _("Welcome to AIMER Portal")

sitemaps = {
    "posts": PostSitemap,
    "tags": TagSitemap,
}

urlpatterns = i18n_patterns(
    path(
        "admin/statuscheck/", include("celerybeat_status.urls")
    ),  # celerybeat_status admin
    path("admin/", admin.site.urls),  # django admin
    path("captcha/", include("captcha.urls")),  # Captcha
    path('', include("chatbot.urls", namespace='chatbot')),
    path("", include("pages.urls")),
    path("", include("website.urls", namespace="website")),
    path("auth/", include("authentication.urls", namespace="auth")),
    path("blog/", include("blog.urls", namespace="blog")),
    path("faq/", include("faq.urls", namespace="faq")),
    path("rosetta/", include("rosetta.urls")),  # Translation
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    # path('ticket/', include('ticket.urls', namespace='ticket')),
    path("tutorial/", include("tutorial.urls", namespace="tutorial")),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler404 = custom_404_view
handler403 = custom_403_view
handler400 = custom_400_view
handler500 = custom_500_view
