from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('greatwar.postcards.views',
    url(r'^$', 'browse', name='browse'),
    url(r'^about/$', 'summary', name='index'),    
    url(r'^(?P<pid>[^/]+)$', 'view_postcard', name='card'),
    url(r'^(?P<pid>[^/]+)/thumbnail/$', 'thumbnail_image', name='img-thumb'),
    url(r'^(?P<pid>[^/]+)/medium/$', 'medium_image', name='img-medium'),
    url(r'^(?P<pid>[^/]+)/large/$', 'large_image', name='img-large'),
    url(r'^search/$', 'search', name='search'),
    #url(r'^search/$', 'searchform'),

    
)
 
