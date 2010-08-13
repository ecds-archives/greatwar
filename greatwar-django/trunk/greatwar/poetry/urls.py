from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('greatwar.poetry.views',
    url(r'^$', 'books', name='books'),
    url(r'^poet$', 'poets'),
    url(r'^poet/(?P<letter>[A-Z]*)$', 'poets_by_firstletter'),
    url(r'^poet/(?P<name>.*)$', 'poet_list'),
    url(r'^(?P<doc_id>[^/]+)$', 'book_toc'),
    url(r'^(?P<doc_id>[^/]+)/(?P<div_id>[a-zA-Z_0-9]+)$', 'div'),
)
 
