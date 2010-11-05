from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('greatwar.postcards.views',
    url(r'^$', 'browse', name='browse'),
    url(r'^about/$', 'summary', name='index'),    
    url(r'^(?P<pid>[^/]+)$', 'view_postcard', name='card'),
    url(r'^(?P<pid>[^/]+)/thumbnail/$', 'postcard_image', {'size': 'thumbnail'}, name='img-thumb'),
    url(r'^(?P<pid>[^/]+)/medium/$', 'postcard_image', {'size': 'medium'}, name='img-medium'),
    url(r'^(?P<pid>[^/]+)/large/$', 'postcard_image', {'size': 'large'}, name='img-large'),
    url(r'^search/$', 'search', name='search'),
    #url(r'^search/$', 'searchform'),

    
)
 
