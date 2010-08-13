from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^greatwar/', include('greatwar.foo.urls')),
    url(r'^poetry/', include('greatwar.poetry.urls', namespace='poetry')),
    url(r'^postcards/', include('greatwar.postcards.urls', namespace='postcards')),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
          
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^(?P<path>(?:css|icons|javascripts|images)/.*)$', 'serve',
            {'document_root': '../media'})
    )
 
