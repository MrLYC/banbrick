from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

urlpatterns = patterns(
    '',
    url("favicon.ico", RedirectView.as_view(url="static/favicon.ico")),

    url(r'^panel/', include('xpanel.urls')),
)
