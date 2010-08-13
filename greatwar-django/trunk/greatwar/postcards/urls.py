from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('greatwar.postcards.views',
    url(r'^$', 'index', name='index'),
    url(r'^view/$', 'postcards', name='browse'),
    url(r'^card/(?P<entity>[-A-Za-z_0-9]+)$', 'card'),
    url(r'^about/$', 'about', name='about'),
    url(r'^search/$', 'searchform'),

    ## experimental fedora-based version of postcards
    url(r'^repo/$', 'fedora_postcards', name='repo-browse'),
    url(r'^repo/(?P<pid>[^/]+)$', 'repo_postcard', name='repo-view'),
    url(r'^repo/(?P<pid>[^/]+)/thumbnail$', 'repo_thumbnail', name='img-thumb'),
    url(r'^repo/(?P<pid>[^/]+)/medium$', 'repo_medium_img', name='img-medium'),
    url(r'^repo/(?P<pid>[^/]+)/large$', 'repo_large_img', name='img-large'),
#    (r'^poet$', 'poets'),
#    (r'^poet/(?P<letter>[A-Z]*)$', 'poets_by_firstletter'),                       
#    (r'^poet/(?P<name>.*)$', 'poet_list'),
#    (r'^(?P<doc_id>[^/]+)$', 'book_toc'),
#    (r'^(?P<doc_id>[^/]+)/(?P<div_id>[a-zA-Z_0-9]+)$', 'div'),
)
 
