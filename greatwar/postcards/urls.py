from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('greatwar.postcards.views',
    (r'^$', 'postcards'),
    (r'^postcards$', 'introduction'),                   
#    (r'^poet$', 'poets'),
#    (r'^poet/(?P<letter>[A-Z]*)$', 'poets_by_firstletter'),                       
#    (r'^poet/(?P<name>.*)$', 'poet_list'),
#    (r'^(?P<doc_id>[^/]+)$', 'book_toc'),
#    (r'^(?P<doc_id>[^/]+)/(?P<div_id>[a-zA-Z_0-9]+)$', 'div'),
)
 
