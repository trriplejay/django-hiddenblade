from django.conf.urls import patterns, url
from . import views
#from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', views.RosterListView.as_view(), name="list"),
    url(r'^(?P<pk>/<slug>[\w-]+)/$', views.RosterDetailView.as_view(), name="detail")
)
