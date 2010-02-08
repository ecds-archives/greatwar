from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('greatwar.poetry.views',
    (r'^$', 'books'),
    (r'^(?P<docname>[^/]+)$', 'book_toc'),
    (r'^(?P<docname>[^/]+)/(?P<div_id>[a-zA-Z_0-9]+)$', 'div'),
)
 
