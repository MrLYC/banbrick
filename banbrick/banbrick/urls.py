from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

urlpatterns = patterns(
    '',
    url(r'favicon.ico', RedirectView.as_view(url='static/favicon.ico')),

    url(r'^panel/', include('xpanel.urls')),
    url(r'^api/', include('apis.urls')),

    url(r'', RedirectView.as_view(url='panel/')),
)
