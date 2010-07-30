from django.conf.urls.defaults import patterns

urlpatterns = patterns('greatwar.postcards.views',
    (r'^$', 'index'),
    (r'^view/$', 'postcards'),
    (r'^card/(?P<entity>[-A-Za-z_0-9]+)$', 'card'),
    (r'^about/$', 'about'),
    (r'^search/$', 'searchform'),

    ## experimental fedora-based version of postcards
    (r'^repo/$', 'fedora_postcards'),
    (r'^repo/(?P<pid>[^/]+)$', 'repo_postcard'),
    (r'^repo/(?P<pid>[^/]+)/thumbnail$', 'repo_thumbnail'),
    (r'^repo/(?P<pid>[^/]+)/medium$', 'repo_medium_img'),
    (r'^repo/(?P<pid>[^/]+)/large$', 'repo_large_img'),
#    (r'^poet$', 'poets'),
#    (r'^poet/(?P<letter>[A-Z]*)$', 'poets_by_firstletter'),                       
#    (r'^poet/(?P<name>.*)$', 'poet_list'),
#    (r'^(?P<doc_id>[^/]+)$', 'book_toc'),
#    (r'^(?P<doc_id>[^/]+)/(?P<div_id>[a-zA-Z_0-9]+)$', 'div'),
)
 
