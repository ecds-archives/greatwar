from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from greatwar import views


admin.autodiscover()

urlpatterns = [
    # Example:
    url(r'^$', views.index, name="index"),
    url(r'^$', views.index, name="site-index"), # required by eultheme
    url(r'^about/$', views.about, name="about"),
    url(r'^links/$', views.links, name="links"),
    url(r'^credits/$', views.credits, name="credits"),
    url(r'^poetry/', include('greatwar.poetry.urls', namespace='poetry')),
    url(r'^postcards/', include('greatwar.postcards.urls', namespace='postcards')),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # django admin, for downtime/banners
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEV_ENV:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


