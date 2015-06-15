from django.conf.urls.defaults import *
from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^greatwar/', include('greatwar.foo.urls')),
    url(r'^$', 'greatwar.views.index', name="index"),
    url(r'^about/$', 'greatwar.views.about', name="about"),
    url(r'^links/$', 'greatwar.views.links', name="links"),
    url(r'^credits/$', 'greatwar.views.credits', name="credits"),
    url(r'^poetry/', include('greatwar.poetry.urls', namespace='poetry')),
    url(r'^postcards/', include('greatwar.postcards.urls', namespace='postcards')),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),

)

if settings.DEV_ENV:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


