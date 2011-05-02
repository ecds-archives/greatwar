from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('greatwar.poetry.views',
    url(r'^$', 'books', name='books'),
    url(r'^search/$', 'search', name='search'),
    url(r'^poet/$', 'poets', name="poets"),
    url(r'^poet/(?P<letter>[A-Z]*)$', 'poets_by_firstletter', name="poets-by-letter"),
    url(r'^poet/(?P<name>.*)$', 'poet_list', name="poet-list"),
    url(r'^(?P<doc_id>[^/]+)/$', 'book_toc', name="book-toc"),
    url(r'^(?P<doc_id>[^/]+)/TEI/$', 'book_xml', name="book-xml"),
    url(r'^(?P<doc_id>[^/]+)/(?P<div_id>[a-zA-Z_0-9]+)/', 'div', name="poem"),
    
)
 
