from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from rest_framework.documentation import include_docs_urls
from drf_yasg import openapi
from blog.sitemaps import BlogSitemap
from .sitemaps import StaticViewSitemap
from django.contrib.sitemaps.views import sitemap
from comment.sitemaps import CommentViewSitemap
import debug_toolbar
from blog.feeds import LatestEntriesFeed

sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
    'contact':CommentViewSitemap
}

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls", namespace="blog")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("comment/", include("comment.urls", namespace="comment")),
    path("", views.IndexPage.as_view(), name="index"),
    path("api-auth/", include("rest_framework.urls")),
    path("api-docs/", include_docs_urls(title="api sample")),
    path("swagger/", schema_view.with_ui("swagger"), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc"), name="schema-redoc"),
    path("swagger/api.json", schema_view.without_ui(), name="schema-json"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt',include('robots.urls')),
    path('summernote/',include('django_summernote.urls')),
    path('captcha',include('captcha.urls')),
    path('rss/feed/',LatestEntriesFeed()),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
