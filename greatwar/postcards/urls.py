from django.conf.urls import url
from django.views.decorators.cache import cache_page

from greatwar.postcards import views

urlpatterns = [
    url(r'^$', views.browse, name='browse'),
    url(r'^about/$', views.summary, name='index'),
    url(r'^categories/(?P<subject>.*)$', views.browse, name='browse'),
    url(r'^(?P<pid>[^/]+)$', views.view_postcard, name='card'),
    url(r'^large/(?P<pid>[^/]+)$', views.view_postcard_large, name='card-large'),
    url(r'^(?P<pid>[^/]+)/thumbnail/$', views.postcard_image, {'size': 'thumbnail'}, name='img-thumb'),
    url(r'^(?P<pid>[^/]+)/medium/$', views.postcard_image, {'size': 'medium'}, name='img-medium'),
    url(r'^(?P<pid>[^/]+)/large/$', views.postcard_image, {'size': 'large'}, name='img-large'),
    url(r'^search/$', views.search, name='search'),
]

