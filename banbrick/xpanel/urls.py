from django.conf.urls import patterns, include, url
import xadmin

xadmin.autodiscover()

urlpatterns = patterns(
    'panel',

    url(r'^', include(xadmin.site.urls)),
)
