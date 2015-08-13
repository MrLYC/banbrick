from django.conf.urls import patterns, include, url
import xadmin

xadmin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'banbrick.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include(xadmin.site.urls), name='xpanel'),
)
