from django.conf.urls import url

from greatwar.poetry import views

urlpatterns = [
    url(r'^$', views.books, name='books'),
    url(r'^search/$', views.search, name='search'),
    url(r'^poet/$', views.poets, name="poets"),
    url(r'^poet/(?P<letter>[A-Z]*)$', views.poets_by_firstletter, name="poets-by-letter"),
    url(r'^poet/(?P<name>.*)$', views.poet_list, name="poet-list"),
    url(r'^(?P<doc_id>[^/]+)/$', views.book_toc, name="book-toc"),
    url(r'^(?P<doc_id>[^/]+)/TEI/$', views.book_xml, name="book-xml"),
    url(r'^(?P<doc_id>[^/]+)/(?P<div_id>[a-zA-Z_0-9]+)/', views.div, name="poem"),
]
