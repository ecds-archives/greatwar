from django.conf.urls.defaults import *
from edc import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/home/html/greatWar/templates/'}),
	(r'^about/$', 'edc.search.views.about'),
	(r'^credits/$', 'edc.search.views.credits'),
	(r'^poetrysearch/advanced/$', 'edc.search.views.advancedSearch'),
	(r'^poetry/volume_browse/$', 'edc.search.views.volume_browse'),
	(r'^poetry/volume/(?P<volfile>\w+)/$', 'edc.search.views.volumeContent'),
	(r'^poetry/front/(?P<div_id>\w+)/$', 'edc.search.views.front_detail'),
	(r'^poetry/(?P<parent_type>\w+)/(?P<poem_id>\w+)/$', 'edc.search.views.poem_detail'),
	(r'^poetry/poem/(?P<poem_id>\w+)/$', 'edc.search.views.poem_detail'),
	(r'^$', 'edc.search.views.opening_page'),
	(r'^postcards$', 'edc.search.views.underconstruction'),
	(r'^links$', 'edc.search.views.underconstruction'),
        (r'^poetry/Poet_browse/$', 'edc.search.views.underconstruction'),
)
