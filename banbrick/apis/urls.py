from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from . import views

urlpatterns = patterns(
    '',
    url(r'^auth?/$', views.api_auth_view),
    url(r'^monitoritems/collector/?$', views.ItemCollectorView.as_view()),
)
