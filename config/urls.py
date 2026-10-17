from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from apps.core.sitemaps import ArticleSitemap, BlogSitemap, StaticViewSitemap, SubjectSitemap
from apps.core.views import robots_txt

sitemaps = {
    'static': StaticViewSitemap,
    'subjects': SubjectSitemap,
    'articles': ArticleSitemap,
    'blog': BlogSitemap,
}

# Rebrand the real Django admin at /sd/ — replaces "Django administration"
# in the header, browser tab title, and index page heading.
admin.site.site_header = 'THE BASICS Admin'
admin.site.site_title = 'THE BASICS Admin'
admin.site.index_title = 'Site Administration'

urlpatterns = [
    # Django's real (model-generated) admin moved off the guessable /admin/
    # path to /sd/. /admin/ is now the real content-management dashboard,
    # built to match the site's own look — gated to staff/superusers by
    # every view's StaffRequiredMixin; non-staff who land here get bounced
    # to their own dashboard, not a 403.
    path('sd/', admin.site.urls),
    path('admin/', include('apps.platform_admin.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('subjects/', include('apps.content.urls')),
    path('prelims/', include('apps.prelims.urls')),
    path('bookmarks/', include('apps.engagement.urls')),
    path('mains/', include('apps.mains.urls')),
    path('evaluations/', include('apps.evaluations.urls')),
    path('current-affairs/', include('apps.current_affairs.urls')),
    path('blog/', include('apps.blog.urls')),
    path('billing/', include('apps.billing.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('', include('apps.core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
